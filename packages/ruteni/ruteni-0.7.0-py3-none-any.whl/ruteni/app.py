from typing import Optional

from starlette.datastructures import State

from ruteni.core.app import Application
from ruteni.core.lifespan import Lifespan
from ruteni.core.types import HTTPApp, HTTPNode, WebSocketApp, WebSocketNode
from ruteni.responses import http_response, not_a_websocket
from ruteni.routers import HTTPNodeRouter, WebSocketNodeRouter
from ruteni.service import Service
from ruteni.status import NOT_FOUND_404
from ruteni.tasks import Tasks


class Ruteni(Application):
    def __init__(
        self,
        http_node: Optional[HTTPNode] = None,
        websocket_node: Optional[WebSocketNode] = None,
        *,
        services: Optional[set[str]] = None
    ) -> None:
        state = State()
        tasks = Tasks(state)
        lifespan_app = Lifespan(tasks)

        if services is not None:
            Service.load_entry_points(services)
            tasks.on_startup(Service.start_services)
            tasks.on_shutdown(Service.stop_services)

        http_app: HTTPApp = http_response[NOT_FOUND_404]
        if http_node is not None:
            http_app = HTTPNodeRouter(http_node)

        websocket_app: WebSocketApp = not_a_websocket
        if websocket_node is not None:
            websocket_app = WebSocketNodeRouter(websocket_node)

        super().__init__(http_app, websocket_app, lifespan_app)
