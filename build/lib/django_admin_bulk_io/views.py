from logging import getLogger

from django.apps import apps
from django.core.files.base import ContentFile
from django.db.models import Model, QuerySet
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from django_admin_bulk_io.serializer import BulkIODynamicSerializer
from django_admin_bulk_io.utils.constants import (
    AcceptedTypes,
    BulkIOException,
    BulkIOMessages,
    Keys,
    LogMessages,
)
from django_admin_bulk_io.utils.exceptions import (
    EmptyFile,
    FileTypeNotSupported,
    InvalidFileContent,
    RequestBodyEmpty,
)
from django_admin_bulk_io.utils.response import JsonResponseRenderer
from django_admin_bulk_io.utils.utils import (
    filter_data_from_csv,
    generate_csv_filename,
    generate_csv_from_data,
    generate_csv_from_serialized_data,
    log_messages,
    save_csv_file_in_base_dir,
    validate_data_from_csv_file,
)

logger = getLogger(__name__)


def get_model(app_label: str, model_name: str) -> Model:
    """
    This method returns model class for given app label and model name.
    """
    return apps.get_model(app_label=app_label, model_name=model_name)


BulkIOExport = get_model(app_label="django_admin_bulk_io", model_name="BulkIOExport")
BulkIOImport = get_model(app_label="django_admin_bulk_io", model_name="BulkIOImport")


@method_decorator(csrf_exempt, name="dispatch")
class BulkIOBaseView(View):
    import_model = BulkIOImport
    export_model = BulkIOExport
    renderer = JsonResponseRenderer
    serializer_class = BulkIODynamicSerializer

    def create_import_model_file(self, file):
        return self.import_model.objects.create(file=file)

    def create_export_model_file(self, file: ContentFile):
        return self.export_model.objects.create(file=file)

    def request_body_empty(self) -> JsonResponse:
        raise RequestBodyEmpty(BulkIOException.REQUEST_BODY_EMPTY)

    def get_serializer(self):
        self.serializer_class.Meta.model = self.model
        return self.serializer_class

    def dispatch(self, request, *args, **kwargs):
        self.app_label, self.model_name, self.action = [
            path for path in self.request.path.split("/") if path not in ["", "admin"]
        ]
        self.model = get_model(app_label=self.app_label, model_name=self.model_name)
        return super().dispatch(request, *args, **kwargs)


class BulkImportValidateBase(BulkIOBaseView):

    def validate_file_content_type(self, file):
        if file.content_type not in AcceptedTypes.get_accepted_types_list():
            raise FileTypeNotSupported(BulkIOException.FILE_TYPE_NOT_SUPPORTED)

    def is_file_empty(self, file):
        if not file.size:
            raise EmptyFile(BulkIOException.FILE_EMPTY)

    def post(self, request, *args, **kwargs):
        if not request.FILES:
            self.request_body_empty()
        file = request.FILES["file"]
        self.validate_file_content_type(file=file)
        self.is_file_empty(file=file)
        return file


class BulkImportView(BulkImportValidateBase):

    def post(self, request, *args, **kwargs):
        try:
            file = super(BulkImportView, self).post(request, *args, **kwargs)
            data = NotImplementedError
            data = filter_data_from_csv(model=self.model, csv_str=file)
            if not data:
                raise InvalidFileContent(BulkIOException.INVALID_CSV_FILE)
            self.create_import_model_file(file=file)
            serializer = self.get_serializer()
            errors = []
            for item in data:
                s = serializer(data=item)
                if s.is_valid():
                    s.save()
                else:
                    errors.append(s.errors)
                    log_messages(error=s.errors, logger=logger.warning)
            message = BulkIOMessages.CSV_IMPORTED_SUCCESSFULLY % (
                len(data) - len(errors),
            )
            if errors:
                log_message = LogMessages.VIEW_LOG_FOR_DETAILS
                message = BulkIOMessages.CSV_IMPORTED_WITH_EXCEPTIONS % (
                    len(data) - len(errors),
                    log_message,
                )
            return self.renderer.render_ok(data={"message": message})
        except EmptyFile as ef:
            return self.renderer.render_bad_request(data={"message": str(ef)})
        except FileTypeNotSupported as ftnse:
            return self.renderer.render_bad_request(data={"message": str(ftnse)})
        except InvalidFileContent as icf:
            return self.renderer.render_bad_request(data={"message": str(icf)})
        except RequestBodyEmpty as rbe:
            return self.renderer.render_bad_request(data={"message": str(rbe)})
        except Exception as err:
            log_messages(
                error=LogMessages.UNKNOWN_EXCEPTION_OCCURED % str(err),
                logger=logger.error,
            )
            return self.renderer.render_internal_server_error(
                data={"message": BulkIOException.UNKNOWN_EXCEPTION_OCCURED},
            )


bulk_import_view = BulkImportView.as_view()


class BulkValidateView(BulkImportValidateBase):

    def post(self, request, *args, **kwargs):
        try:
            file = super(BulkValidateView, self).post(request, *args, **kwargs)
            data = validate_data_from_csv_file(model=self.model, csv_str=file)
            if not data:
                raise InvalidFileContent(BulkIOException.INVALID_CSV_FILE)
            errors = 0
            serializer = self.get_serializer()
            validated_data = []
            for item in data:
                s = serializer(data=item)
                if s.is_valid():
                    item["action"] = "created"
                    validated_data.append(item)
                else:
                    errors += 1
                    item["action"] = "skipped"
                    item["erros"] = ", ".join(
                        [
                            f"{field}:{error[0].code}"
                            for field, error in s.errors.items()
                        ]
                    )
                    validated_data.append(item)

            csv = generate_csv_from_data(data=validated_data)
            save_csv_file_in_base_dir(
                csv_str=csv, info=(self.app_label, self.model_name)
            )
            return self.renderer.render_ok(
                data={"message": BulkIOMessages.CSV_VALIDATED_SUCCESSFULLY % errors}
            )
        except EmptyFile as ef:
            return self.renderer.render_bad_request(data={"message": str(ef)})
        except FileTypeNotSupported as ftnse:
            return self.renderer.render_bad_request(data={"message": str(ftnse)})
        except InvalidFileContent as icf:
            return self.renderer.render_bad_request(data={"message": str(icf)})
        except RequestBodyEmpty as rbe:
            return self.renderer.render_bad_request(data={"message": str(rbe)})
        except Exception as err:
            log_messages(
                error=LogMessages.UNKNOWN_EXCEPTION_OCCURED % str(err),
                logger=logger.error,
            )
            return self.renderer.render_internal_server_error(
                data={"message": BulkIOException.UNKNOWN_EXCEPTION_OCCURED},
            )


bulk_validate_view = BulkValidateView.as_view()


class BulkExportView(BulkIOBaseView):
    def get_queryset(self):
        return self.model.objects.all()

    def get_queryset_with_ids(self, queryset: QuerySet, ids: list) -> QuerySet:
        return queryset.filter(pk__in=ids)

    def post(self, request, *args, **kwargs):
        try:
            if not request.POST:
                self.request_body_empty()
            queryset = self.get_queryset()
            if Keys.SELECT_ALL not in request.POST:
                payload = request.POST.get(Keys.SELECTED_ACTION).split(",")
                if not payload:
                    self.request_body_empty()
                queryset = self.get_queryset_with_ids(queryset=queryset, ids=payload)
            data = self.get_serializer()(queryset, many=True).data
            csv_str = generate_csv_from_serialized_data(data=data)
            title = generate_csv_filename()
            file = self.create_export_model_file(
                file=ContentFile(content=csv_str, name=title)
            )
            return self.renderer.render_ok(
                data={
                    "message": BulkIOMessages.CSV_CREATED_SUCCESSFULLY,
                    "file": {"url": file.url, "title": file.title},
                },
            )
        except RequestBodyEmpty as rbe:
            return self.renderer.render_bad_request(data={"message": str(rbe)})
        except (KeyError, ValueError):
            return self.renderer.render_bad_request(
                data={"message": BulkIOException.INVALID_REQUEST_BODY},
            )
        except Exception as err:
            log_messages(
                error=LogMessages.UNKNOWN_EXCEPTION_OCCURED % str(err),
                logger=logger.error,
            )
            return self.renderer.render_internal_server_error(
                data={"message": BulkIOException.UNKNOWN_EXCEPTION_OCCURED},
            )


bulk_export_view = BulkExportView.as_view()
