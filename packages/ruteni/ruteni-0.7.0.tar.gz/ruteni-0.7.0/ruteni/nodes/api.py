from collections.abc import Iterable, MutableSet
from typing import Optional

from ruteni.core.types import Node
from ruteni.nodes import ExtractorNode, IterableNode
from ruteni.service import Service, ServiceSet
from starlette.datastructures import State
from ruteni.extractors import PrefixExtractor


class APINode(ExtractorNode, Service):
    def __init__(
        self,
        name: str,
        version: int,
        children: Iterable[Node],
        requires: Optional[ServiceSet] = None,
    ) -> None:
        ExtractorNode.__init__(
            self, PrefixExtractor(f"/{name}/v{version}"), IterableNode(children)
        )
        Service.__init__(self, name, version, requires)

    async def startup(self, state: State) -> None:
        await Service.startup(self, state)
        api_nodes.add(self)

    async def shutdown(self, state: State) -> None:
        await Service.shutdown(self, state)
        api_nodes.remove(self)


api_nodes: MutableSet[APINode] = set()
