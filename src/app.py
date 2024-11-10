import sys
import os
from flask import Flask, send_from_directory, jsonify
from flask_restful import Api
from flask_cors import CORS
from config.config import Config
from flask_restful import Resource

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from flask_swagger_ui import get_swaggerui_blueprint
from players.handlers import Players, PlayerDetail
from players.service import PlayersService
from players.store import PlayersStore
from teams.handlers import Teams, TeamDetail
from teams.store import TeamsStore
from teams.service import TeamsService
from db.connection import get_db_connection
from competitions.handlers import Competitions
from competitions.service import CompetitionsService
from competitions.store import CompetitionsStore
from areas.handlers import Areas, AreaDetail
from areas.service import AreasService
from areas.store import AreasStore
from matches.handlers import Matches
from matches.service import MatchesService
from matches.store import MatchesStore

app = Flask(__name__)
app.config.from_object(Config)

CORS(app, resources={r"/api/*": {"origins": "http://localhost:5173"}})

api = Api(app)

db_connection = get_db_connection()

players_store = PlayersStore(db_connection=db_connection)
players_service = PlayersService(store=players_store)

teams_store = TeamsStore(db_connection=db_connection)
teams_service = TeamsService(store=teams_store)

competitions_store = CompetitionsStore(db_connection=db_connection)
competitions_service = CompetitionsService(store=competitions_store)

areas_store = AreasStore(db_connection=db_connection)
areas_service = AreasService(store=areas_store)

matches_store = MatchesStore(db_connection=db_connection)
matches_service = MatchesService(store=matches_store)

api.add_resource(Teams, '/api/teams', '/api/teams/', resource_class_args=(teams_service,))
api.add_resource(TeamDetail, '/api/teams/<string:id>', resource_class_args=(teams_service,))
api.add_resource(Players, '/api/players', '/api/players/', resource_class_args=(players_service,))
api.add_resource(PlayerDetail, '/api/players/<string:id>', resource_class_args=(players_service,))
api.add_resource(Matches, '/api/matches', '/api/matches/', resource_class_args=(matches_service,))
api.add_resource(Competitions, '/api/competitions', '/api/competitions/', resource_class_args=(competitions_service,))
api.add_resource(Areas, '/api/areas', '/api/areas/', resource_class_args=(areas_service,))
api.add_resource(AreaDetail, '/api/areas/<string:area_id>', resource_class_args=(areas_service,))

SWAGGER_URL = '/api/docs'  
API_URL = '/swagger/openapi.yaml'  

swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={'app_name': "FanPulse API"}
)
app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

@app.route('/swagger/openapi.yaml')
def serve_openapi_yaml():
    return send_from_directory(os.path.join(app.root_path, '..', 'swagger'), 'openapi.yaml')

if __name__ == '__main__':
    app.run(debug=True)
