import sys
import os
import pytest
import uuid
from unittest.mock import MagicMock
from players.service import PlayersService
from players.store import PlayersStore
from app import app

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

@pytest.fixture
def mock_players_service():
    mock_store = MagicMock(PlayersStore)
    mock_service = PlayersService(store=mock_store)
    return mock_service

def test_get_all_players(client, mock_players_service, monkeypatch):
    sample_players = [
        {
            "id": "a3691360-1150-480f-9c36-5ce8bf134536",
            "jersey_number": 0,
            "name": "Russell Westbrook",
            "player_image_url": "https://upload.wikimedia.org/wikipedia/commons/b/be/Russell_Westbrook_%28March_21%2C_2022%29_%28cropped%29.jpg",
            "position": "Guard"
        },
        {
            "id": "7ba7d9ea-d8c6-4ca7-91e2-f42af1ac6c4a",
            "jersey_number": 3,
            "name": "Anthony Davis",
            "player_image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/36/Anthony_Davis_pre-game_%28cropped%29.jpg/640px-Anthony_Davis_pre-game_%28cropped%29.jpg",
            "position": "Forward-Center"
        }
    ]
    monkeypatch.setattr(mock_players_service, "fetch_all_players", lambda: sample_players)
    response = client.get("/api/players")
    assert response.status_code == 200
    assert all(player in response.json for player in sample_players)

def test_get_player_detail(client, mock_players_service, monkeypatch):
    player_id = "a3691360-1150-480f-9c36-5ce8bf134536"
    sample_player_detail = {
        "country_name": None,
        "date_of_birth": "Sat, 12 Nov 1988 00:00:00 GMT",
        "height_cm": 191,
        "id": player_id,
        "jersey_number": 0,
        "name": "Russell Westbrook",
        "player_image_url": "https://upload.wikimedia.org/wikipedia/commons/b/be/Russell_Westbrook_%28March_21%2C_2022%29_%28cropped%29.jpg",
        "position": "Guard",
        "social_media": {
            "facebook": "https://facebook.com/kingjames",
            "instagram": "https://instagram.com/kingjames",
            "twitter": "https://twitter.com/KingJames",
            "youtube": None
        },
        "stats": {
            "assists_per_game": "8.2",
            "blocks_per_game": "0.6",
            "field_goal_percentage": "50.4",
            "free_throw_percentage": "80.0",
            "games_played": 1020,
            "minutes_per_game": "38.1",
            "personal_fouls_per_game": "2.0",
            "points_per_game": "27.2",
            "rebounds_per_game": "7.5",
            "steals_per_game": "1.3",
            "three_point_percentage": "34.5",
            "turnovers_per_game": "3.5"
        },
        "team_id": "d161bb3d-45ac-4f79-8882-38ea487493fe",
        "weight_kg": 91
    }
    monkeypatch.setattr(mock_players_service, "fetch_player_details", lambda x: sample_player_detail if x == player_id else None)
    response = client.get(f"/api/players/{player_id}")
    assert response.status_code == 200
    assert response.json == sample_player_detail

def test_get_player_detail_not_found(client, mock_players_service, monkeypatch):
    non_existent_id = str(uuid.uuid4())
    monkeypatch.setattr(mock_players_service, "fetch_player_details", lambda x: None)
    response = client.get(f"/api/players/{non_existent_id}")
    assert response.status_code == 404
    assert response.json == {"error": "Player not found"}
