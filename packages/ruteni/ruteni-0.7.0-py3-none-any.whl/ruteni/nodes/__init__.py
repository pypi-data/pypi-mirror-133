from __future__ import annotations

import logging
from collections.abc import (
    Callable,
    Collection,
    Iterable,
    Iterator,
    Mapping,
    MutableSequence,
)
from typing import Generic, Optional, cast

from asgiref.typing import HTTPScope, WebSocketScope
from pkg_resources import load_entry_point
from ruteni.core.types import (
    App,
    Extractor,
    HTTPReceive,
    HTTPSend,
    Node,
    TReceive,
    TScope,
    TSend,
    URLPath,
    WebSocketApp,
)
from ruteni.responses import http_response
from ruteni.status import METHOD_NOT_ALLOWED_405
from ruteni.types import (
    AcceptRoute,
    HTTPAppMap,
    Method,
    ReadEndpoint,
    Route,
    WriteEndpoint,
)
from starlette.responses import RedirectResponse

logger = logging.getLogger(__name__)


def current_path(route: Route) -> URLPath:
    return route[-1][0]


def current_path_is(url_path: URLPath) -> AcceptRoute:
    return lambda route: current_path(route) == url_path


def current_path_in(url_paths: Collection[URLPath]) -> AcceptRoute:
    return lambda route: current_path(route) in url_paths


def load_http_node_entry_point(dist: str, name: str) -> Node[HTTPScope]:
    return load_entry_point(dist, "ruteni.node.http.v1", name)


def load_websocket_node_entry_point(dist: str, name: str) -> Node[WebSocketScope]:
    return load_entry_point(dist, "ruteni.node.websocket.v1", name)


class HTTPNode:
    def __init__(self, accept_route: AcceptRoute, app_map: HTTPAppMap) -> None:
        self.accept_route = accept_route
        self.app_map = app_map

    async def __call__(self, scope: HTTPScope, route: Route) -> Optional[App]:
        return (
            self.app_map.get(
                cast(Method, scope["method"]), http_response[METHOD_NOT_ALLOWED_405]
            )
            if self.accept_route(route)
            else None
        )


def GET(endpoint: ReadEndpoint) -> HTTPAppMap:
    async def app(scope: HTTPScope, receive: HTTPReceive, send: HTTPSend) -> None:
        response = await endpoint(scope)
        await response(scope, receive, send)

    return dict(GET=app)


def POST(endpoint: WriteEndpoint) -> HTTPAppMap:
    async def app(scope: HTTPScope, receive: HTTPReceive, send: HTTPSend) -> None:
        response = await endpoint(scope, receive)
        await response(scope, receive, send)

    return dict(POST=app)


class WebSocketNode:
    def __init__(self, accept_route: AcceptRoute, app: WebSocketApp) -> None:
        self.accept_route = accept_route
        self.app = app

    async def __call__(self, scope: WebSocketScope, route: Route) -> Optional[App]:
        return self.app if self.accept_route(route) else None


class IterableNode(Generic[TScope]):
    def __init__(self, nodes: Iterable[Node]) -> None:
        # TODO: assert nodes can be iterated multiple times (e.g. not a generator)
        self.nodes = nodes

    def __repr__(self) -> str:
        return "%s()" % self.__class__.__name__

    async def __call__(self, scope: TScope, route: Route) -> Optional[App]:
        for node in self.nodes:
            response = await node(scope, route)
            if response is not None:
                return response
        return None


class MappingNode(Generic[TScope]):
    def __init__(self, node_map: Mapping[URLPath, Node]) -> None:
        self.node_map = node_map

    def __repr__(self) -> str:
        return "%s()" % self.__class__.__name__

    async def __call__(self, scope: TScope, route: Route) -> Optional[App]:
        url_path = current_path(route)
        for prefix, node in self.node_map.items():
            if url_path == prefix or url_path.startswith(prefix + "/"):
                route_elem = (url_path.removeprefix(prefix), prefix)
                route.append(route_elem)
                response = await node(scope, route)
                if response is None:
                    route.pop()
                return response
        return None


class NodeStat:
    def __init__(self) -> None:
        self.hits = 0
        self.misses = 0


class StatsNode(Iterable[Node], Generic[TScope, TReceive, TSend]):
    def __init__(self, nodes: Iterable[Node]) -> None:
        self.children = [(node, NodeStat()) for node in nodes]

    def __repr__(self) -> str:
        return "%s()" % self.__class__.__name__

    async def __call__(self, scope: TScope, route: Route) -> Optional[App]:
        for node, stat in self.children:
            response = await node(scope, route)
            if response is not None:
                stat.hits += 1
                return response
            else:
                stat.misses += 1
        return None

    def __iter__(self) -> Iterator[Node]:
        return (node for node, stat in self.children)

    def add_child(self, node: Node) -> None:
        self.children.append((node, NodeStat()))

    def remove_child(self, node: Node) -> None:
        for child in self.children:
            if child[0] == node:
                self.children.remove(child)
                break

    def reorder(self) -> None:
        self.children.sort(key=lambda child: child[1].hits, reverse=True)


class ExtractorNode:
    def __init__(self, extractor: Extractor, child: Node) -> None:
        self.extractor = extractor
        self.child = child

    def __repr__(self) -> str:
        return super().__repr__()[:-1] + ", extractor=%r)" % self.extractor

    async def __call__(self, scope: TScope, route: Route) -> Optional[App]:
        route_elem = self.extractor(current_path(route))
        if route_elem is None:
            return None
        route.append(route_elem)
        response = await self.child(scope, route)
        if response is None:
            route.pop()
        return response


class RedirectNode:
    def __init__(self, accept_route: AcceptRoute, url_path: URLPath) -> None:
        self.accept_route = accept_route
        self.url_path = url_path

    def __repr__(self) -> str:
        return "%s(url_path=%r)" % (self.__class__.__name__, self.url_path)

    async def __call__(self, scope: HTTPScope, route: Route) -> Optional[App]:
        return RedirectResponse(self.url_path) if self.accept_route(route) else None


class SlashRedirectNode:
    def __repr__(self) -> str:
        return "%s()" % (self.__class__.__name__)

    async def __call__(self, scope: HTTPScope, route: Route) -> Optional[App]:
        return (
            RedirectResponse(scope["path"] + "/") if current_path(route) == "" else None
        )
