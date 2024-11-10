from .store import CompetitionsStore
from typing import List, Dict, Union

class CompetitionsService:
    def __init__(self, store: CompetitionsStore):
        self.store = store

    def fetch_competitions(self) -> List[Dict[str, Union[str, Dict]]]:
        competitions = self.store.get_competitions()
        
        return [
            {
                'id': str(comp['id']),
                'name': comp['name'],
                'type': comp['type'],
                'season': comp['season'],
                'icon_url': comp['icon_url'],
                'country': {
                    'name': comp['country_name'],
                    'image_url': comp['country_image_url']
                },
                'league': {
                    'name': comp['league_name'],
                    'icon_url': comp['league_icon_url']
                }
            }
            for comp in competitions
        ]
