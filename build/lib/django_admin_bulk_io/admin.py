# Django Admin Bulk I/O Admin

from django.contrib.admin import ModelAdmin, site
from django.urls import path

from django_admin_bulk_io.models import BulkIOExport, BulkIOImport
from django_admin_bulk_io.views import (
    bulk_export_view,
    bulk_import_view,
    bulk_validate_view,
)

site.register(BulkIOExport)
site.register(BulkIOImport)


class BulkIOModelAdmin(ModelAdmin):
    def get_urls(self, *args, **kwargs):
        """
        This method overrides existing get_urls method to returns urls for bulk import and export.
        """
        info = self.opts.app_label, self.opts.model_name
        urls = super(BulkIOModelAdmin, self).get_urls(*args, **kwargs)
        bulk_io_urls = [
            path(
                "bulk-validate/", bulk_validate_view, name="%s_%s_bulk_validate" % info
            ),
            path("bulk-import/", bulk_import_view, name="%s_%s_bulk_import" % info),
            path("bulk-export/", bulk_export_view, name="%s_%s_bulk_export" % info),
        ]
        return bulk_io_urls + urls
