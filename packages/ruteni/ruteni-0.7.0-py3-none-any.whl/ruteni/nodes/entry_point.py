from collections.abc import Mapping

from ruteni.endpoints import (
    load_http_endpoint_entry_point,
    load_websocket_endpoint_entry_point,
)
from ruteni.nodes import HTTPNode, WebSocketNode
from ruteni.types import AcceptRoute, Method


class HTTPEntryPointNode(HTTPNode):
    def __init__(
        self, accept_route: AcceptRoute, entry_map: Mapping[Method, tuple[str, str]]
    ) -> None:
        super().__init__(
            accept_route,
            {
                method: load_http_endpoint_entry_point(*info)
                for method, info in entry_map.items()
            },
        )


class WebSocketEntryPointNode(WebSocketNode):
    def __init__(self, accept_route: AcceptRoute, dist: str, name: str) -> None:
        super().__init__(accept_route, load_websocket_endpoint_entry_point(dist, name))
