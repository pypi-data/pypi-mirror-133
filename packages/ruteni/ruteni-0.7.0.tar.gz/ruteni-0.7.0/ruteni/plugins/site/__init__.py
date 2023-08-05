from pkg_resources import resource_filename
from ruteni.config import config
from starlette.endpoints import HTTPEndpoint
from starlette.requests import Request
from starlette.responses import FileResponse, Response

ABUSE_URL: str = config.get("RUTENI_VERIFICATION_ABUSE_URL")
SITE_NAME: str = config.get("RUTENI_SITE_NAME")
SITE_DOMAIN: str = config.get("RUTENI_SITE_DOMAIN")
LOGO_PATH: str = config.get(
    "RUTENI_SITE_LOGO_PATH", default=resource_filename(__name__, "/resources/logo.svg")
)
FAVICON_PATH: str = config.get(
    "RUTENI_SITE_FAVICON_PATH",
    default=resource_filename(__name__, "/resources/favicon.ico"),
)

# TODO: use an Icon from ruteni.utils.icon


class Favicon(HTTPEndpoint):
    # favicon = b64decode(
    #     "AAABAAEAEBACAAEAAQBWAAAAFgAAAIlQTkcNChoKAAAADUlIRFIAAAAQAAAAEAgGAAAAH/P/"
    #     "YQAAAB1JREFUOI1j/P///38GCgATJZpHDRg1YNSAwWQAAGvKBByn4XVTAAAAAElFTkSuQmCC"
    # )
    async def get(self, request: Request) -> Response:
        return FileResponse(FAVICON_PATH, media_type="image/x-icon")
        # return Response(Favicon.favicon, media_type="image/x-icon")
