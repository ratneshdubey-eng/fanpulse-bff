from flask_restful import Resource
from .service import CompetitionsService
from helpers.responses import success_response

class Competitions(Resource):
    def __init__(self, service: CompetitionsService):
        self.service = service

    def get(self):
        competitions = self.service.fetch_competitions()
        return success_response(competitions)


