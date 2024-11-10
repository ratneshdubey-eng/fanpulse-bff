from db.connection import get_db_connection
from typing import List, Dict

class CompetitionsStore:
    def __init__(self, db_connection=None):
        self.db_connection = db_connection or get_db_connection()

    def get_competitions(self) -> List[Dict]:
        query = """
            SELECT 
                competitions.id, 
                competitions.name, 
                competitions.type, 
                competitions.season, 
                competitions.icon_url,
                countries.name AS country_name, 
                countries.image_url AS country_image_url,
                leagues.name AS league_name, 
                leagues.icon_url AS league_icon_url
            FROM competitions
            LEFT JOIN countries ON competitions.country_id = countries.id
            LEFT JOIN leagues ON competitions.league_id = leagues.id
        """
        
        with self.db_connection.cursor() as cursor:
            cursor.execute(query)
            competitions = cursor.fetchall()
        
        return competitions
