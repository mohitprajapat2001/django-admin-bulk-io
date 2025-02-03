# Custom Django Admin Bulk IO Exceptions


class RequestBodyEmpty(Exception):
    pass


class FileTypeNotSupported(Exception):
    pass


class InvalidFileContent(Exception):
    pass


class EmptyFile(Exception):
    pass
