import os

from starlette.applications import Starlette
from starlette.routing import Mount
from starlette.staticfiles import StaticFiles

from solidctf.service import create_asgi_application

project_root = os.getcwd()
if os.environ.get("DEBUG_MODE", False):
    project_root = os.path.join(project_root, "example")

routes = [
    Mount("/api", app=create_asgi_application(project_root)),
    Mount("/", app=StaticFiles(directory="web/dist", html=True)),
]

app = Starlette(routes=routes)
