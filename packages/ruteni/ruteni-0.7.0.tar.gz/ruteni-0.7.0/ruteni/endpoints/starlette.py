from asgiref.typing import HTTPScope
from ruteni.core.types import HTTPReceive, HTTPSend

from starlette.middleware.base import RequestResponseEndpoint
from starlette.requests import Request


class StarletteHTTPEndpoint:
    def __init__(self, func: RequestResponseEndpoint) -> None:
        self.func = func

    async def __call__(
        self, scope: HTTPScope, receive: HTTPReceive, send: HTTPSend
    ) -> None:
        request = Request(scope, receive=receive, send=send)
        response = await self.func(request)
        await response(scope, receive, send)
