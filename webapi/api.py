from utils.ai_utils import get_logger
from typeguard import typechecked
from webapi.controllers import *
from flask_restful import Api
from logging import Logger


@typechecked
def logger() -> Logger:
    return get_logger(__name__)


@typechecked
def set_api_resources() -> None:
    api = Api(app)
    api.add_resource(MoveAnalysisController, '/move_analysis')
    api.add_resource(MatchAnalysisController, '/match_analysis')

@typechecked
def start_api(use_port: str) -> None:
    set_api_resources()

    try:
        app.run(port=use_port, threaded=True)
    except:
        logger().exception("Failed to start server")
