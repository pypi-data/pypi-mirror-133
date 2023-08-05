from ruteni.config import config
from ruteni.content import TEXT_PLAIN_CONTENT_TYPE, Content
from ruteni.nodes import current_path_is
from ruteni.nodes.content import HTTPContentNode

ROBOT_TEXT: bytes = config.get(
    "RUTENI_ROBOT_TEXT", cast=str.encode, default="User-agent: *\nDisallow:"
)

node = HTTPContentNode(
    current_path_is("/robots.txt"), Content(ROBOT_TEXT, TEXT_PLAIN_CONTENT_TYPE)
)
