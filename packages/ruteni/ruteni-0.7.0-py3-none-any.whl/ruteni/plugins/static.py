from ruteni.config import config
from ruteni.nodes.static import StaticHTTPNode

directory = config.get("RUTENI_DEVEL_STATIC_DIR")
node = StaticHTTPNode(directory, html=False)
