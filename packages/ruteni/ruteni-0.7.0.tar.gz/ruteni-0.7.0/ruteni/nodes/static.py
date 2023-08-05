import os
import stat
from typing import Optional

import anyio
from asgiref.typing import HTTPScope
from ruteni.core.types import App, Route
from ruteni.nodes import current_path
from ruteni.responses import http_response
from ruteni.status import BAD_REQUEST_400, METHOD_NOT_ALLOWED_405, NOT_FOUND_404
from ruteni.types import PathLike
from starlette.responses import FileResponse


class StaticHTTPNode:
    def __init__(self, directory: PathLike, *, html: bool = False) -> None:
        stat_result = os.stat(directory)
        assert stat.S_ISDIR(stat_result.st_mode)
        self.directory = os.path.realpath(directory)

    def __repr__(self) -> str:
        root_dir = os.path.dirname(os.path.dirname(__file__))  # TODO: fragile
        path = os.path.relpath(self.directory, root_dir)
        return "%s(directory=%r)" % (self.__class__.__name__, path)

    async def __call__(self, scope: HTTPScope, route: Route) -> Optional[App]:
        url_path = current_path(route)
        if len(url_path) == 0 or url_path[0] != "/":
            return http_response[BAD_REQUEST_400]

        if scope["method"] != "GET":
            return http_response[METHOD_NOT_ALLOWED_405]

        full_path = os.path.realpath(os.path.join(self.directory, url_path[1:]))

        # test that the path is indeed a descendant of our directory, to prevent
        # requests using .. from going too far up the hierarchy
        if os.path.commonprefix([full_path, self.directory]) != self.directory:
            return http_response[BAD_REQUEST_400]

        # get the stat info for the file, and detect if it does not exist
        try:
            stat_result = await anyio.to_thread.run_sync(os.stat, full_path)
        except FileNotFoundError:
            return http_response[NOT_FOUND_404]

        # we don't serve directory content
        if stat.S_ISDIR(stat_result.st_mode):
            return http_response[BAD_REQUEST_400]

        return FileResponse(full_path, stat_result=stat_result)
