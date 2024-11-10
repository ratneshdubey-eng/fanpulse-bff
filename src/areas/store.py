import psycopg2.extras
from db.connection import get_db_connection
from typing import List, Dict

class AreasStore:
    def __init__(self, db_connection=None):
        self.db_connection = db_connection or get_db_connection()

    def get_all_areas(self) -> List[Dict]:
        query = """
            SELECT area_id as id, name, image_url as image, location
            FROM areas
        """
        
        with self.db_connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
            cursor.execute(query)
            areas = cursor.fetchall()
        
        return areas

    def get_area_by_id(self, area_id: str) -> List[Dict]:
        query = """
            SELECT 
                a.area_id as id, 
                a.name, 
                a.location, 
                a.image_url as image,
                c.name as country_name,
                c.image_url as country_image,
                ac.capacity_type,
                ac.capacity_count,
                af.facility_name,
                af.description as facility_description,
                e.event_name,
                e.event_date,
                e.description as event_description
            FROM areas a
            LEFT JOIN countries c ON a.country_id = c.id
            LEFT JOIN area_capacity ac ON a.area_id = ac.area_id
            LEFT JOIN area_facilities af ON a.area_id = af.area_id
            LEFT JOIN area_events e ON a.area_id = e.area_id
            WHERE a.area_id = %s
        """
        
        with self.db_connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
            cursor.execute(query, (area_id,))
            area = cursor.fetchall()
        
        return area
