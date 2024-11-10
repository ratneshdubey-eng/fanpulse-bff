from typing import List, Dict, Optional, Union
from .store import PlayersStore

class PlayersService:
    def __init__(self, store: PlayersStore):
        self.store = store

    def fetch_all_players(self) -> List[Dict[str, Union[str, int]]]:
        players = self.store.get_all_players()
        return [self._transform_basic_player(player) for player in players]

    def fetch_player_details(self, player_id: str) -> Optional[Dict[str, Union[str, Dict]]]:
        player = self.store.get_player_by_id(player_id)
        if not player:
            return None
        return self._transform_detailed_player(player)

    def _transform_basic_player(self, player: Dict) -> Dict[str, Union[str, int]]:
        return {
            'id': str(player['id']),
            'name': player['name'],
            'position': player['position'],
            'jersey_number': player['jersey_number'],
            'player_image_url': player['player_image_url']
        }

    def _transform_detailed_player(self, player: Dict) -> Dict[str, Union[str, Dict]]:
        return {
            'id': str(player['id']),
            'name': player['name'],
            'position': player['position'],
            'jersey_number': player['jersey_number'],
            'team_id': str(player['team_id']),
            'player_image_url': player['player_image_url'],
            'date_of_birth': player.get('date_of_birth'),
            'height_cm': player.get('height_cm'),
            'weight_kg': player.get('weight_kg'),
            'country_name': player.get('country_name'),
            'stats': self._transform_stats(player),
            'social_media': self._transform_social_media(player)
        }

    def _transform_stats(self, player: Dict) -> Dict[str, Union[str, int]]:
        return {
            'games_played': player.get('games_played'),
            'minutes_per_game': player.get('minutes_per_game'),
            'field_goal_percentage': player.get('field_goal_percentage'),
            'three_point_percentage': player.get('three_point_percentage'),
            'free_throw_percentage': player.get('free_throw_percentage'),
            'rebounds_per_game': player.get('rebounds_per_game'),
            'assists_per_game': player.get('assists_per_game'),
            'blocks_per_game': player.get('blocks_per_game'),
            'steals_per_game': player.get('steals_per_game'),
            'personal_fouls_per_game': player.get('personal_fouls_per_game'),
            'turnovers_per_game': player.get('turnovers_per_game'),
            'points_per_game': player.get('points_per_game')
        } if player.get('games_played') is not None else {}

    def _transform_social_media(self, player: Dict) -> Dict[str, Optional[str]]:
        return {
            'twitter': player.get('twitter'),
            'instagram': player.get('instagram'),
            'facebook': player.get('facebook'),
            'youtube': player.get('youtube')
        } if player.get('twitter') is not None else {}
