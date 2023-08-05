from http import HTTPStatus

from ruteni.core.types import HTTPApp
from ruteni.responses import http_response


class HTTPException(Exception):
    def __init__(self, status: HTTPStatus) -> None:
        self.status = status

    def __repr__(self) -> str:
        class_name = self.__class__.__name__
        return (
            f"{class_name}(status={self.status.value!r}, detail={self.status.phrase!r})"
        )

    @property
    def response(self) -> HTTPApp:
        return http_response[self.status]
