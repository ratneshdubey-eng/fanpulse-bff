import pytest
from unittest.mock import MagicMock
from players.service import PlayersService
from players.store import PlayersStore

@pytest.fixture
def mock_players_store():
    return MagicMock(PlayersStore)

@pytest.fixture
def players_service(mock_players_store):
    return PlayersService(store=mock_players_store)

def test_fetch_all_players(players_service, mock_players_store):
    sample_players = [
        {
            "id": "a3691360-1150-480f-9c36-5ce8bf134536",
            "name": "Russell Westbrook",
            "position": "Guard",
            "jersey_number": 0,
            "player_image_url": "https://upload.wikimedia.org/wikipedia/commons/b/be/Russell_Westbrook_%28March_21%2C_2022%29_%28cropped%29.jpg"
        },
        {
            "id": "7ba7d9ea-d8c6-4ca7-91e2-f42af1ac6c4a",
            "name": "Anthony Davis",
            "position": "Forward-Center",
            "jersey_number": 3,
            "player_image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/36/Anthony_Davis_pre-game_%28cropped%29.jpg/640px-Anthony_Davis_pre-game_%28cropped%29.jpg"
        }
    ]
    mock_players_store.get_all_players.return_value = sample_players

    players = players_service.fetch_all_players()
    assert players == [
        {
            "id": "a3691360-1150-480f-9c36-5ce8bf134536",
            "name": "Russell Westbrook",
            "position": "Guard",
            "jersey_number": 0,
            "player_image_url": "https://upload.wikimedia.org/wikipedia/commons/b/be/Russell_Westbrook_%28March_21%2C_2022%29_%28cropped%29.jpg"
        },
        {
            "id": "7ba7d9ea-d8c6-4ca7-91e2-f42af1ac6c4a",
            "name": "Anthony Davis",
            "position": "Forward-Center",
            "jersey_number": 3,
            "player_image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/36/Anthony_Davis_pre-game_%28cropped%29.jpg/640px-Anthony_Davis_pre-game_%28cropped%29.jpg"
        }
    ]
    mock_players_store.get_all_players.assert_called_once()

def test_fetch_player_details(players_service, mock_players_store):
    player_id = "a3691360-1150-480f-9c36-5ce8bf134536"
    sample_player_detail = {
        "id": player_id,
        "name": "Russell Westbrook",
        "position": "Guard",
        "jersey_number": 0,
        "team_id": "d161bb3d-45ac-4f79-8882-38ea487493fe",
        "player_image_url": "https://upload.wikimedia.org/wikipedia/commons/b/be/Russell_Westbrook_%28March_21%2C_2022%29_%28cropped%29.jpg",
        "date_of_birth": "Sat, 12 Nov 1988 00:00:00 GMT",
        "height_cm": 191,
        "weight_kg": 91,
        "country_name": None,
        "games_played": 1020,
        "minutes_per_game": "38.1",
        "field_goal_percentage": "50.4",
        "three_point_percentage": "34.5",
        "free_throw_percentage": "80.0",
        "rebounds_per_game": "7.5",
        "assists_per_game": "8.2",
        "blocks_per_game": "0.6",
        "steals_per_game": "1.3",
        "personal_fouls_per_game": "2.0",
        "turnovers_per_game": "3.5",
        "points_per_game": "27.2",
        "twitter": "https://twitter.com/KingJames",
        "instagram": "https://instagram.com/kingjames",
        "facebook": "https://facebook.com/kingjames",
        "youtube": None
    }

    mock_players_store.get_player_by_id.return_value = sample_player_detail

    expected_player_detail = {
        "id": player_id,
        "name": "Russell Westbrook",
        "position": "Guard",
        "jersey_number": 0,
        "team_id": "d161bb3d-45ac-4f79-8882-38ea487493fe",
        "player_image_url": "https://upload.wikimedia.org/wikipedia/commons/b/be/Russell_Westbrook_%28March_21%2C_2022%29_%28cropped%29.jpg",
        "date_of_birth": "Sat, 12 Nov 1988 00:00:00 GMT",
        "height_cm": 191,
        "weight_kg": 91,
        "country_name": None,
        "stats": {
            "games_played": 1020,
            "minutes_per_game": "38.1",
            "field_goal_percentage": "50.4",
            "three_point_percentage": "34.5",
            "free_throw_percentage": "80.0",
            "rebounds_per_game": "7.5",
            "assists_per_game": "8.2",
            "blocks_per_game": "0.6",
            "steals_per_game": "1.3",
            "personal_fouls_per_game": "2.0",
            "turnovers_per_game": "3.5",
            "points_per_game": "27.2"
        },
        "social_media": {
            "twitter": "https://twitter.com/KingJames",
            "instagram": "https://instagram.com/kingjames",
            "facebook": "https://facebook.com/kingjames",
            "youtube": None
        }
    }

    player_detail = players_service.fetch_player_details(player_id)
    assert player_detail == expected_player_detail
    mock_players_store.get_player_by_id.assert_called_once_with(player_id)
