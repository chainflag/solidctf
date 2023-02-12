import os

from twirp.asgi import TwirpASGIApp

from eth_challenge_base.config import parse_config
from eth_challenge_base.protobuf import challenge_twirp
from eth_challenge_base.service import ChallengeService


def create_service(project_path: str = "."):
    if os.getenv("APP_ENV") == "development":
        project_path = "example"
    project_path = os.path.join(os.path.dirname(__file__), project_path)
    config = parse_config(os.path.join(project_path, "challenge.yml"))
    return challenge_twirp.ChallengeServer(
        service=ChallengeService(project_path, config)
    )


service = create_service()
app = TwirpASGIApp()
app.add_service(service)
