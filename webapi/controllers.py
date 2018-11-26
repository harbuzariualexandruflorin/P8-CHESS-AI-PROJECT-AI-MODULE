from flask_restful import Resource
from werkzeug.utils import redirect
from webapi.services import *
from flask import Flask
import json

app = Flask(__name__)


@app.route('/')
def home():
    return redirect("/chess/1")


class ChessController(Resource):

    def __init__(self):
        self.chess_service = ChessService()

    def get(self, id):
        test = self.chess_service.get_service()
        test = id
        response = app.response_class(
            response=json.dumps(test),
            status=200,
            mimetype='application/json'
        )
        return response

    def post(self, id):
        test = self.chess_service.post_service()
        response = app.response_class(
            response=json.dumps(test),
            status=200,
            mimetype='application/json'
        )
        return response
