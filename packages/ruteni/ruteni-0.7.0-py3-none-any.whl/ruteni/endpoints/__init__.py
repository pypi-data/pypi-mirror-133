from pkg_resources import load_entry_point
from ruteni.core.types import HTTPApp, WebSocketApp


def load_http_endpoint_entry_point(dist: str, name: str) -> HTTPApp:
    return load_entry_point(dist, "ruteni.endpoint.http.v1", name)


def load_websocket_endpoint_entry_point(dist: str, name: str) -> WebSocketApp:
    return load_entry_point(dist, "ruteni.endpoint.websocket.v1", name)
