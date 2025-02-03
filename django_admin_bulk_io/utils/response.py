from http import HTTPStatus

from django.http import JsonResponse


class JsonResponseRenderer:
    @classmethod
    def render_response(cls, data: dict, status: int) -> JsonResponse:
        """
        This method renders the json response.
        """
        return JsonResponse(data=data, status=status)

    @classmethod
    def render_not_found(cls, data: dict):
        return cls.render_response(data=data, status=HTTPStatus.NOT_FOUND)

    @classmethod
    def render_bad_request(cls, data: dict):
        return cls.render_response(data=data, status=HTTPStatus.BAD_REQUEST)

    @classmethod
    def render_internal_server_error(cls, data: dict):
        return cls.render_response(data=data, status=HTTPStatus.INTERNAL_SERVER_ERROR)

    @classmethod
    def render_ok(cls, data: dict):
        return cls.render_response(data=data, status=HTTPStatus.OK)
