from django.db.models import Model, FileField, DateTimeField


def _upload_to(self, filename):
    return f"bulk_io/{self.__class__.__name__.lower()}/{filename}"


class BulkIOFiles(Model):
    file = FileField(max_length=1024, upload_to=_upload_to)
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)

    @property
    def url(self):
        return self.file.url

    @property
    def title(self):
        return self.file.name

    class Meta:
        abstract = True


class BulkIOExport(BulkIOFiles):
    pass

    def __str__(self):
        return self.title


class BulkIOImport(BulkIOFiles):
    pass

    def __str__(self):
        return self.title
