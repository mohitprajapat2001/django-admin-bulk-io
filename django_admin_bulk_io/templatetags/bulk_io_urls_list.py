from django import template
from django.template import Library
from django.urls import reverse
from django.utils.safestring import mark_safe

register = Library()


def bulk_io_reverse(app_label, model_name, path_template: str):
    """returns bulk io url reverse based on app_label & model_name directly"""

    url_name = path_template % (app_label, model_name)
    url = reverse(f"admin:{url_name}")
    return url


@register.simple_tag(name="bulk_io_urls")
def do_bulk_io_urls(*args):
    """
    This template tag renders the bulk import and export links for a given model.
    """
    app_label, model_name, path = args
    return BulkIOUrlsNode(app_label, model_name, path).render()


@register.simple_tag
def bulk_io_url(*args):
    app_label, model_name, path = args
    try:
        url = bulk_io_reverse(app_label, model_name, path)
        return url
    except Exception:
        pass


class BulkIOUrlsNode(template.Node):
    def __init__(self, app_label, model_name, path):
        self.app_label = app_label
        self.model_name = model_name
        self.path = path

    def render(self, *args):
        try:
            url_export = bulk_io_reverse(self.app_label, self.model_name, self.path)
            return mark_safe(
                """
                    <li>
                        <button class="btn"
                            onclick="bulkIOExport(event, '%s')">
                                <span class="text">Export</span><span>Download CSV</span>
                        </button>
                    </li>
                    <li>
                        <button class="btn" data-bs-toggle="modal" data-bs-target="#bulkIoAdminModalRead">
                            <span class="text">Import</span><span>Read CSV</span>
                        </button>
                    </li>
                    <li>
                        <button class="btn" data-bs-toggle="modal" data-bs-target="#bulkIoAdminModalValidate">
                            <span class="text">Check</span><span>Validate CSV</span>
                        </button>
                    </li>
                """
                % (url_export)
            )
        except Exception:
            return ""
