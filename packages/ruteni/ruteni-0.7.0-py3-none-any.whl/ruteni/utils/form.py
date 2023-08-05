import io
import json
import urllib
from cgi import parse_multipart
from collections.abc import Container
from typing import Any, Optional, Type

from asgiref.typing import HTTPScope
from marshmallow import Schema
from marshmallow.exceptions import ValidationError
from ruteni.core.types import HTTPReceive
from ruteni.exceptions import HTTPException
from ruteni.status import (
    BAD_REQUEST_400,
    UNPROCESSABLE_ENTITY_422,
    UNSUPPORTED_MEDIA_TYPE_415,
)
from starlette import status
from starlette.requests import Request
from starlette.responses import Response
from werkzeug.http import parse_options_header


async def get_body(request: Request) -> Response:
    content_type_header = request.headers.get("Content-Type")
    content_type, options = parse_options_header(content_type_header)
    if content_type == b"application/json":
        try:
            return await request.json()
        except json.decoder.JSONDecodeError:
            return Response(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)
    elif (
        content_type == b"multipart/form-data"
        or content_type == b"application/x-www-form-urlencoded"
    ):
        try:
            return await request.form()
        except TypeError:
            return Response(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)
    else:
        return Response(status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)


async def get_form(request: Request, Schema: Type[Schema]) -> Optional[dict]:
    body = await get_body(request)
    schema = Schema()
    try:
        return schema.load(body)
    except ValidationError:
        return None


def get_content_type_header(scope: HTTPScope) -> Optional[bytes]:
    for key, val in scope["headers"]:
        if key == b"content-type":
            return val
    return None


async def get_chunk(receive: HTTPReceive) -> bytes:
    event = await receive()

    if event["type"] == "http.disconnect":
        raise HTTPException(BAD_REQUEST_400)

    assert event["type"] == "http.request"

    # TODO: if the server is really ASGI compliant, both event["body"] and
    # event["more_body"] should be defined, but uvicorn may not define those
    if "body" not in event or event.get("more_body", False):
        raise HTTPException(BAD_REQUEST_400)

    return event["body"]


def parse_content_type(
    header: Optional[bytes], allowed_types: Optional[Container] = None
) -> tuple[str, dict[str, str]]:
    if header is None:
        raise HTTPException(UNSUPPORTED_MEDIA_TYPE_415)

    content_type, options = parse_options_header(
        header.decode("latin-1"), multiple=False
    )

    if allowed_types and content_type not in allowed_types:
        raise HTTPException(UNSUPPORTED_MEDIA_TYPE_415)

    return content_type, options


def extract_form(body: bytes, content_type: str, options: dict[str, str]) -> dict:
    if content_type == "application/json":
        try:
            raw_form = json.loads(body)
        except json.decoder.JSONDecodeError:
            raise HTTPException(UNPROCESSABLE_ENTITY_422)
    elif content_type == "multipart/form-data":
        raw_form = parse_multipart(io.BytesIO(body), dict(boundary=b"--"))  # options
        if len(raw_form) == 0:  # TODO: detect errors
            raise HTTPException(UNPROCESSABLE_ENTITY_422)
    elif content_type == "application/x-www-form-urlencoded":
        raw_form = {
            key.decode(): val[0].decode()
            for key, val in urllib.parse.parse_qs(body).items()
        }

    return raw_form


async def receive_form(
    content_type_header: Optional[bytes], receive: HTTPReceive
) -> dict[str, Any]:
    content_type, options = parse_content_type(
        content_type_header,
        (
            "application/json",
            "multipart/form-data",
            "application/x-www-form-urlencoded",
        ),
    )
    # we only allow one chunk; convert to a loop if this can be a problem
    body = await get_chunk(receive)
    return extract_form(body, content_type, options)


async def get_form2(
    content_type_header: Optional[bytes], receive: HTTPReceive, Schema: type[Schema]
) -> dict:
    raw_form = await receive_form(content_type_header, receive)
    schema = Schema()
    try:
        return schema.load(raw_form)
    except ValidationError:
        raise HTTPException(BAD_REQUEST_400)


async def get_json_body(
    scope: HTTPScope,
    receive: HTTPReceive,
    content_type: Optional[bytes] = b"application/json",
) -> dict:
    if get_content_type_header(scope) != content_type:  # TODO: relax?
        raise HTTPException(UNSUPPORTED_MEDIA_TYPE_415)
    body = await get_chunk(receive)  # TODO: use loop version
    # TODO: have a marshmallow schema to validate report?
    try:
        return json.loads(body.decode("utf-8"))
    except json.decoder.JSONDecodeError:
        raise HTTPException(UNPROCESSABLE_ENTITY_422)
