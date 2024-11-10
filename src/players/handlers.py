from flask import jsonify
from flask_restful import Resource
from helpers.validators import is_valid_uuid
from helpers.responses import error_response, success_response
from players.service import PlayersService

class Players(Resource):
    def __init__(self, service: PlayersService):
        self.players_service = service

    def get(self):
        players = self.players_service.fetch_all_players()
        return success_response(players)

class PlayerDetail(Resource):
    def __init__(self, service: PlayersService):
        self.players_service = service

    def get(self, id):
        if not is_valid_uuid(id):
            return error_response("Invalid player ID format", 400)

        player_details = self.players_service.fetch_player_details(id)

        if player_details:
            return success_response(player_details)
        
        return error_response("Player not found", 404)
