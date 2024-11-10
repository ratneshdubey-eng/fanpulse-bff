from .store import AreasStore
from typing import List, Dict, Union, Optional

class AreasService:
    def __init__(self, store: AreasStore):
        self.store = store

    def fetch_all_areas(self) -> List[Dict[str, Union[str, int]]]:
        areas = self.store.get_all_areas()
        return [
            {
                'id': str(area['id']),
                'name': area['name'],
                'location': area['location'],
                'image_url': area['image']
            }
            for area in areas
        ]

    def fetch_area_details(self, area_id: str) -> Optional[Dict[str, Union[str, Dict]]]:
        area_data = self.store.get_area_by_id(area_id)
        
        if not area_data:
            return None
        
        area_info = area_data[0]
        
        capacities = [
            {
                'type': row['capacity_type'],
                'count': row['capacity_count']
            }
            for row in area_data if row['capacity_type'] and row['capacity_count']
        ]
        
        return {
            'area_id': str(area_info['id']),
            'name': area_info['name'],
            'location': area_info['location'],
            'image_url': area_info['image'],
            'country': {
                'name': area_info['country_name'],
                'image_url': area_info['country_image']
            } if area_info['country_name'] else {},
            'capacity': capacities,
            'facilities': list({row['facility_name'] for row in area_data if row['facility_name']}),
            'events': [
                {
                    'event_name': row['event_name'],
                    'event_date': row['event_date']
                }
                for row in area_data if row['event_name']
            ]
        }
