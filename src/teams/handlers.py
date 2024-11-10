from flask import jsonify, abort
from flask_restful import Resource

from helpers.responses import error_response
from helpers.validators import is_valid_uuid
from .service import TeamsService

class Teams(Resource):
    def __init__(self, service: TeamsService):
        self.service = service

    def get(self):
        teams = self.service.fetch_all_teams()
        return teams, 200

class TeamDetail(Resource):
    def __init__(self, service: TeamsService):
        self.service = service

    def get(self, id):
        if not is_valid_uuid(id):
            return error_response("Invalid team ID format", 400)
        team_details = self.service.fetch_team_details(id)
        
        if team_details is None:
            abort(404, description="Team not found")
        
        return jsonify(team_details)
