from .store import TeamsStore
from typing import List, Dict, Optional, Union

class TeamsService:
    def __init__(self, store: TeamsStore):
        self.store = store

    def fetch_all_teams(self) -> List[Dict[str, Union[str, int]]]:
        teams = self.store.get_all_teams()
        return [
            {
                'id': str(team['id']),
                'name': team['name'],
                'logo_url': team['logo_url']
            }
            for team in teams
        ]

    def fetch_team_details(self, team_id: str) -> Optional[Dict[str, Union[str, Dict]]]:
        team_data = self.store.get_team_by_id(team_id)
        
        if not team_data:
            return None
        
        team_info = team_data[0]
        
        return {
            'team_id': team_info['team_id'],
            'name': team_info['team_name'],
            'logo_url': team_info['team_logo'],
            'season_history': [
                {
                    'season': row['season'],
                    'wins': row['wins'],
                    'losses': row['losses'],
                    'draws': row['draws'],
                    'championships': row['championships']
                }
                for row in team_data if row['season']
            ],
            'players': [
                {
                    'player_id': row['player_id'],
                    'name': row['player_name'],
                    'position': row['player_position'],
                    'image_url': row['player_image']
                }
                for row in team_data if row['player_id']
            ]
        }
