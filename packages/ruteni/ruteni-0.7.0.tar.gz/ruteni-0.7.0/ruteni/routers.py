from collections.abc import Iterable
from typing import Generic, Optional

from asgiref.typing import HTTPScope, WebSocketCloseEvent, WebSocketScope

from ruteni.core.types import (
    HTTPReceive,
    HTTPSend,
    HTTPSendEvent,
    Node,
    Route,
    TScope,
    WebSocketReceive,
    WebSocketSend,
)
from ruteni.responses import http_response
from ruteni.status import INTERNAL_SERVER_ERROR_500, NOT_FOUND_404


class BaseRouter(Generic[TScope]):
    def __init__(self, node: Node) -> None:
        self.node = node


class Sender:
    def __init__(self, _send: HTTPSend) -> None:
        self._send = _send
        self.state: Optional[str] = None

    async def send(self, event: HTTPSendEvent) -> None:
        self.state = event["type"]
        await self._send(event)


class HTTPNodeRouter(BaseRouter[HTTPScope]):
    async def __call__(
        self, scope: HTTPScope, receive: HTTPReceive, send: HTTPSend
    ) -> None:
        sender = Sender(send)
        try:
            route: Route = [(scope["path"], None)]
            response = await self.node(scope, route)
            if response is not None:
                await response(scope, receive, sender.send)
            else:
                await http_response[NOT_FOUND_404](scope, receive, sender.send)
        except Exception as exc:
            if sender.state is None:  # no response was initiated
                await http_response[INTERNAL_SERVER_ERROR_500](scope, receive, send)
            raise exc


class WebSocketNodeRouter(BaseRouter[WebSocketScope]):
    async def __call__(
        self, scope: WebSocketScope, receive: WebSocketReceive, send: WebSocketSend
    ) -> None:
        try:
            route: Route = [(scope["path"], None)]
            response = await self.node(scope, route)
            if response is not None:
                await response(scope, receive, send)
            else:
                # TODO: websocket.http.response
                await send(
                    WebSocketCloseEvent(
                        {"type": "websocket.close", "code": 1000, "reason": "not found"}
                    )
                )
        except Exception as exc:
            await send(
                WebSocketCloseEvent(
                    {"type": "websocket.close", "code": 1011, "reason": None}
                )
            )
            raise exc
