import os

from starlette.applications import Starlette
from starlette.routing import Mount, Route
from starlette.staticfiles import StaticFiles

from solidctf.rpc_proxy import rpc_proxy_handler
from solidctf.service import create_asgi_application

project_root = os.getcwd()
if os.environ.get("DEBUG_MODE", False):
    project_root = os.path.join(project_root, "example")

routes = [
    Mount("/api", app=create_asgi_application(project_root)),
    Route("/eth_rpc", endpoint=rpc_proxy_handler, methods=["POST"]),
    Mount("/", app=StaticFiles(directory="web/dist", html=True)),
]

app = Starlette(routes=routes)
