import logging

from starlette.datastructures import State

from ruteni.types import Callback

logger = logging.getLogger(__name__)


class Tasks:
    def __init__(self, state: State) -> None:
        self.state = state
        self.startup_tasks: list[Callback] = []
        self.shutdown_tasks: list[Callback] = []

    async def __aenter__(self) -> None:
        for startup in self.startup_tasks:
            await startup(self.state)

    async def __aexit__(self, *exc_info: object) -> None:
        for shutdown in self.shutdown_tasks:
            try:
                await shutdown(self.state)
            except Exception:
                logger.exception("shutdown")

    def on_startup(self, callback: Callback) -> None:
        self.startup_tasks.append(callback)

    def on_shutdown(self, callback: Callback) -> None:
        self.shutdown_tasks.append(callback)
