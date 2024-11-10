from flask import request
from flask_restful import Resource
from .service import MatchesService
from helpers.responses import success_response

class Matches(Resource):
    def __init__(self, service: MatchesService):
        self.service = service

    def get(self):
        date = request.args.get('date')
        status = request.args.get('status')
        season = request.args.get('season')
        team_name = request.args.get('team_name')
        
        matches = self.service.fetch_matches(date, status, season, team_name)
        
        return success_response(matches)
