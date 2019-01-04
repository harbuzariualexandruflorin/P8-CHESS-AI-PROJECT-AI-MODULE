from flask_restful import Resource
from webapi.services import *
from flask import request, jsonify
from flask import Flask
import json

app = Flask(__name__)


class MoveAnalysisController(Resource):

    def __init__(self):
        self.chess_service = MoveAnalysisService()

    def post(self):
        state_fen = json.loads(request.data.decode())["fen"]
        result = self.chess_service.move_analysis_service(state_fen)

        response = app.response_class(
            response=json.dumps(json.loads(result)),
            status=200,
            mimetype='application/json'
        )
        return response


class MatchAnalysisController(Resource):

    def __init__(self):
        self.chess_service = MatchAnalysisService()

    def post(self):
        moves = json.loads(request.data.decode())["moves"]
        result = self.chess_service.match_analysis_service(moves)

        response = app.response_class(
            response=json.dumps(json.loads(result)),
            status=200,
            mimetype='application/json'
        )
        return response
