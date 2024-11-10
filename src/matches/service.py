from .store import MatchesStore
from typing import List, Dict, Union, Optional

class MatchesService:
    def __init__(self, store: MatchesStore):
        self.store = store

    def fetch_matches(self, date: Optional[str] = None, status: Optional[str] = None, season: Optional[str] = None, team_name: Optional[str] = None) -> List[Dict[str, Union[str, Dict]]]:
        matches = self.store.get_filtered_matches(date, status, season, team_name)
        
        return [
            {
                "id": str(match['id']),
                "country": match['country'],
                "location": match['location'],
                "match_datetime": match['match_datetime'].isoformat() if match['match_datetime'] else None,
                "season": match['season'],
                "status": match['status'],
                "score_team1": match['score_team1'] if match['status'] in ['live', 'completed'] else None,
                "score_team2": match['score_team2'] if match['status'] in ['live', 'completed'] else None,

                "team1": {
                    "id": str(match['team1_id']),
                    "name": match['team1_name'],
                    "logo_url": match['team1_logo_url']
                },

                
                "team2": {
                    "id": str(match['team2_id']),
                    "name": match['team2_name'],
                    "logo_url": match['team2_logo_url']
                },

                "winner": {
                    "id": str(match['winner_id']) if match['status'] == 'completed' and match['winner_id'] else None,
                    "name": match['winner_name'] if match['status'] == 'completed' else None,
                    "logo_url": match['winner_logo_url'] if match['status'] == 'completed' else None
                } if match['status'] == 'completed' else None,

                "league": {
                    "id": str(match['league_id']) if match['league_id'] else None,
                    "name": match['league_name'],
                    "icon_url": match['league_icon_url']
                }
            }
            for match in matches
        ]
