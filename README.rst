Django Admin Bulk IO
====================

This package allows you to import and export data in your Django admin. It supports various formats like CSV, JSON, and XML.

Features
--------

* **Import data:** Easily import data into your Django models from CSV, JSON, and XML files.
* **Export data:** Export data from your Django models to CSV, JSON, and XML files.
* **Admin integration:** Seamlessly integrates with the Django admin interface.
* **Customizable serializers:** Allows customization of how data is serialized and deserialized.
* **Support for related fields:** Handles import/export of related model data.
* **Error handling and reporting:** Provides detailed error messages during import/export operations.

Installation
------------

.. code-block:: bash

    pip install django-admin-bulk-io

Configuration
-------------

1. Add `django_admin_bulk_io` to your `INSTALLED_APPS` in `settings.py`:

    .. code-block:: python

        INSTALLED_APPS = [
            # ... other apps
            'django_admin_bulk_io',
        ]

2. In your `admin.py`, import and use the `BulkImportMixin` and `BulkExportMixin`:

    .. code-block:: python

        from django.contrib import admin
        from django_admin_bulk_io.admin import BulkImportMixin, BulkExportMixin

        @admin.register(YourModel)
        class YourModelAdmin(admin.ModelAdmin):
            pass

Usage
-----

### Import

In the Django admin, navigate to the list view of the model you want to import data into.

1. Click on the "Import" button.
2. Choose the file you want to import and select the format (CSV, JSON, or XML).
3. Click "Import" to begin the import process.

### Export

1. Select the objects you want to export (or select all).
2. From the "Action" dropdown, choose "Export selected objects".
3. Choose the desired export format (CSV, JSON, or XML).

Contributing
------------

Contributions are welcome! Please submit bug reports and pull requests.

License
-------

This project is licensed under the MIT License.

