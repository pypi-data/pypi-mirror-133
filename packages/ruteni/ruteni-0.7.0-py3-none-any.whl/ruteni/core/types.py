from collections.abc import Awaitable, Callable, MutableSequence
from typing import Literal, Optional, Tuple, TypeVar, Union
from uuid import UUID

from asgiref.typing import (
    HTTPDisconnectEvent,
    HTTPRequestEvent,
    HTTPResponseBodyEvent,
    HTTPResponseStartEvent,
    HTTPScope,
    HTTPServerPushEvent,
    LifespanScope,
    LifespanShutdownCompleteEvent,
    LifespanShutdownEvent,
    LifespanShutdownFailedEvent,
    LifespanStartupCompleteEvent,
    LifespanStartupEvent,
    LifespanStartupFailedEvent,
    WebSocketAcceptEvent,
    WebSocketCloseEvent,
    WebSocketConnectEvent,
    WebSocketDisconnectEvent,
    WebSocketReceiveEvent,
    WebSocketResponseBodyEvent,
    WebSocketResponseStartEvent,
    WebSocketScope,
    WebSocketSendEvent,
)
from starlette.datastructures import URLPath

ParamTypeName = Literal["str", "path", "int", "float", "uuid"]
Param = Union[str, URLPath, int, float, UUID]
RouteElem = tuple[URLPath, Optional[Union[Param, Tuple[Param, ...]]]]
Route = MutableSequence[RouteElem]
Extractor = Callable[[URLPath], Optional[RouteElem]]

HTTPReceiveEvent = Union[HTTPRequestEvent, HTTPDisconnectEvent]
HTTPReceive = Callable[[], Awaitable[HTTPReceiveEvent]]
HTTPSendEvent = Union[
    HTTPResponseStartEvent,
    HTTPResponseBodyEvent,
    HTTPServerPushEvent,
    HTTPDisconnectEvent,
]
HTTPSend = Callable[[HTTPSendEvent], Awaitable[None]]
HTTPApp = Callable[[HTTPScope, HTTPReceive, HTTPSend], Awaitable[None]]
HTTPNode = Callable[[HTTPScope, Route], Awaitable[Optional[HTTPApp]]]
HTTPRouter = Callable[[HTTPScope], HTTPApp]

WebSocketReceive = Callable[
    [],
    Awaitable[
        Union[WebSocketConnectEvent, WebSocketReceiveEvent, WebSocketDisconnectEvent]
    ],
]
WebSocketSend = Callable[
    [
        Union[
            WebSocketAcceptEvent,
            WebSocketSendEvent,
            WebSocketResponseStartEvent,
            WebSocketResponseBodyEvent,
            WebSocketCloseEvent,
        ]
    ],
    Awaitable[None],
]
WebSocketApp = Callable[
    [WebSocketScope, WebSocketReceive, WebSocketSend], Awaitable[None]
]
WebSocketNode = Callable[[WebSocketScope, Route], Awaitable[Optional[WebSocketApp]]]
WebSocketRouter = Callable[[WebSocketScope], WebSocketApp]


LifespanReceiveEvent = Union[LifespanStartupEvent, LifespanShutdownEvent]
LifespanReceive = Callable[[], Awaitable[LifespanReceiveEvent]]
LifespanSendEvent = Union[
    LifespanStartupCompleteEvent,
    LifespanStartupFailedEvent,
    LifespanShutdownCompleteEvent,
    LifespanShutdownFailedEvent,
]
LifespanSend = Callable[[LifespanSendEvent], Awaitable[None]]
LifespanApp = Callable[[LifespanScope, LifespanReceive, LifespanSend], Awaitable[None]]

TScope = TypeVar("TScope", HTTPScope, WebSocketScope, LifespanScope)
TReceive = TypeVar("TReceive", HTTPReceive, WebSocketReceive, LifespanReceive)
TSend = TypeVar("TSend", HTTPSend, WebSocketSend, LifespanSend)

# TScope, TReceive, TSend should not be any combination
# https://github.com/python/mypy/issues/3904
# it would be nice if we could do this:
# Receive = {HTTPScope: HTTPReceive, WebSocketScope: WebSocketReceive, LifespanScope: LifespanReceive}
# Send = {HTTPScope: HTTPSend, WebSocketScope: WebSocketSend, LifespanScope: LifespanSend}
# App = Callable[[TScope, Receive[TScope], Send[TScope]], Awaitable[None]]
App = Callable[[TScope, TReceive, TSend], Awaitable[None]]

Node = Callable[[TScope, Route], Awaitable[Optional[App]]]
Router = Callable[[TScope], App]

WWWApp = Union[HTTPApp, WebSocketApp]
ASGIApp = Union[HTTPApp, WebSocketApp, LifespanApp]
