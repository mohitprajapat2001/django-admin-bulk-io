# Django Admin Bulk I/O Constants

FORM_CLASS_BASE = "form-control bg-light text-dark"
FILE_NAME_TEMPLATE = "%s/bulk_io_validations/%s/%s/"


class AcceptedTypes:
    """Bulk IO - File Accepted Content Types"""

    CSV = "text/csv"
    JSON = "application/json"

    @classmethod
    def get_accepted_types_list(cls) -> list:
        return [cls.CSV, cls.JSON]


class Keys:
    """Bulk IO - Request Keys"""

    ACTION_TOGGLE = "action-toggle"
    SELECTED_ACTION = "_selected_action"
    SELECT_ALL = "select_across"


class BulkIOMessages:
    """Bulk IO - Success Messages"""

    CSV_CREATED_SUCCESSFULLY = "CSV Generated Successfully,"
    CSV_IMPORTED_SUCCESSFULLY = "%s New records created."
    CSV_IMPORTED_WITH_EXCEPTIONS = "%s New records created with exceptions. %s"
    CSV_VALIDATED_SUCCESSFULLY = "CSV Validated Successfully, with %s errors."


class BulkIOException:
    """Bulk IO - Exceptions"""

    REQUEST_BODY_EMPTY = "Request body is empty."
    UNKNOWN_EXCEPTION_OCCURED = "Error, Please view log file for details."
    FILE_TYPE_NOT_SUPPORTED = "File type not supported."
    INVALID_CSV_FILE = "Invalid CSV file."
    INVALID_JSON_FILE = "Invalid JSON file."
    INVALID_REQUEST_BODY = "Invalid request body."
    FILE_EMPTY = "File is empty."


class LogMessages:
    """Bulk IO - Log Messages"""

    VIEW_LOG_FOR_DETAILS = "Please view log file for details."
    FILE_TYPE_NOT_SUPPORTED = "File type not supported."
    UNKNOWN_EXCEPTION_OCCURED = "Error, %s"
