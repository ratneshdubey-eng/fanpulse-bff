import pytest
from unittest.mock import MagicMock
from teams.handlers import Teams, TeamDetail
from flask import Flask

sample_team_data = [
    {
        "id": "d161bb3d-45ac-4f79-8882-38ea487493fe",
        "name": "Los Angeles Lakers",
        "logo_url": "https://upload.wikimedia.org/wikipedia/commons/3/3c/Los_Angeles_Lakers_logo.svg"
    },
    {
        "id": "ca5b22ef-9a8e-4923-839e-41b487c32b62",
        "name": "Golden State Warriors",
        "logo_url": "https://upload.wikimedia.org/wikipedia/en/0/01/Golden_State_Warriors_logo.svg"
    },
]

@pytest.fixture
def app():
    app = Flask(__name__)
    app.testing = True
    return app

@pytest.fixture
def mock_teams_service():
    mock_service = MagicMock()
    mock_service.fetch_all_teams.return_value = sample_team_data
    mock_service.fetch_team_details.return_value = sample_team_data[0]
    return mock_service

@pytest.fixture
def teams_resource(mock_teams_service):
    return Teams(service=mock_teams_service)

@pytest.fixture
def team_detail_resource(mock_teams_service):
    return TeamDetail(service=mock_teams_service)

def test_get_all_teams(app, teams_resource):
    with app.test_request_context():
        data, status_code = teams_resource.get()
        assert status_code == 200
        assert data == sample_team_data

def test_get_team_detail(app, team_detail_resource):
    with app.test_request_context():
        response = team_detail_resource.get("d161bb3d-45ac-4f79-8882-38ea487493fe")
        assert response.status_code == 200
        assert response.get_json() == sample_team_data[0]
