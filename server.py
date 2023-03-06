import os

from eth_challenge_base.service import create_asgi_application

project_root = os.getcwd()
if os.environ.get("DEBUG_MODE", False):
    project_root = os.path.join(project_root, "example")
app = create_asgi_application(project_root)
