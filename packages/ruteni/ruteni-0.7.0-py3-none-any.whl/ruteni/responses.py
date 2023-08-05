from collections.abc import Iterable
from http import HTTPStatus
from typing import Optional

from asgiref.typing import (
    HTTPResponseBodyEvent,
    HTTPResponseStartEvent,
    HTTPScope,
    WebSocketCloseEvent,
    WebSocketScope,
)
from starlette.status import HTTP_200_OK

from ruteni.content import TEXT_PLAIN_CONTENT_TYPE, Content
from ruteni.core.types import HTTPReceive, HTTPSend, WebSocketReceive, WebSocketSend
from ruteni.types import Header


class Response:
    def __init__(
        self,
        content: Optional[Content] = None,
        *,
        headers: Optional[Iterable[Header]] = None,
        status: int = HTTP_200_OK
    ) -> None:
        self.status = status
        self.headers = tuple(headers) if headers else ()
        self.set_content(content or Content(b"", b"application/octet-stream"))

    def set_content(self, content: Content) -> None:
        # TODO: `headers` could be a tuple but it raises an exception in uvicorn
        headers = list(
            self.headers
            + (
                (b"content-length", str(len(content.body)).encode("latin-1")),
                (b"content-type", content.content_type),
            )
        )
        self.start_event = HTTPResponseStartEvent(
            {
                "type": "http.response.start",
                "status": self.status,
                "headers": headers,
            }
        )
        self.body_event = HTTPResponseBodyEvent(
            {"type": "http.response.body", "body": content.body, "more_body": False}
        )

    async def __call__(
        self, scope: HTTPScope, receive: HTTPReceive, send: HTTPSend
    ) -> None:
        await send(self.start_event)
        await send(self.body_event)


http_response = {
    x: Response(Content(x.phrase.encode("utf-8"), TEXT_PLAIN_CONTENT_TYPE), status=x)
    for x in HTTPStatus
}


class WebSocketClose:
    def __init__(self, reason: Optional[str] = None, code: int = 1000) -> None:
        self.event = WebSocketCloseEvent(
            {"type": "websocket.close", "code": code, "reason": reason}
        )

    async def __call__(
        self, scope: WebSocketScope, receive: WebSocketReceive, send: WebSocketSend
    ) -> None:
        await send(self.event)


not_a_websocket = WebSocketClose("Not Found")  # TODO: better name
