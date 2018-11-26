from flask_restful import Api
from webapi.controllers import *
from main.ai_utils import get_logger


def logger():
    return get_logger(__name__)


def set_api_resources():
    api = Api(app)
    api.add_resource(ChessController, '/chess/<id>')


def start_api(use_port):
    set_api_resources()

    try:
        app.run(port=use_port)
    except:
        logger().exception("Failed to start server")
