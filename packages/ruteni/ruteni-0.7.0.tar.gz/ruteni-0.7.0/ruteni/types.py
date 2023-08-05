import os
from collections.abc import Awaitable, Callable, Iterable, Mapping
from typing import Literal, Optional, Union

from asgiref.typing import HTTPScope
from starlette.datastructures import State

from ruteni.core.types import HTTPApp, HTTPReceive, Route

PathLike = Union[str, os.PathLike[str]]

Callback = Callable[[State], Awaitable[None]]

# from starlette.middleware.cors import ALL_METHODS
# ALL_METHODS: typing.tuple[Method, ...] = typing.get_args(Method)
Method = Literal["DELETE", "GET", "HEAD", "OPTIONS", "PATCH", "POST", "PUT"]
Methods = set[Method]
Header = tuple[bytes, bytes]
Headers = Iterable[Header]
HTTPAppMap = Mapping[Method, HTTPApp]
ReadEndpoint = Callable[[HTTPScope], Awaitable[HTTPApp]]
WriteEndpoint = Callable[[HTTPScope, HTTPReceive], Awaitable[HTTPApp]]

# from starlette.convertors import CONVERTOR_TYPES
# CONVERTOR_TYPES keys: ["str", "path", "int", "float", "uuid"]
# from werkzeug.routing import DEFAULT_CONVERTERS
# DEFAULT_CONVERTERS keys: ["default", "string", "any", "path", "int", "float", "uuid"]
AcceptRoute = Callable[[Route], bool]
FileMatchTest = Callable[[HTTPScope, Route], Optional[PathLike]]
