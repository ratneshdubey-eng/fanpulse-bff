from db.connection import get_db_connection
import psycopg2
import psycopg2.extras
from typing import List, Dict

class TeamsStore:
    def __init__(self, db_connection=None):
        self.db_connection = db_connection or get_db_connection()

    def get_all_teams(self) -> List[Dict]:
        query = "SELECT id, name, logo_url FROM teams;"
        
        with self.db_connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
            cursor.execute(query)
            teams = cursor.fetchall()
        
        return teams

    def get_team_by_id(self, team_id: str) -> List[Dict]:
        query = """
            SELECT 
                t.id AS team_id, 
                t.name AS team_name, 
                t.logo_url AS team_logo,
                th.season, 
                th.wins, 
                th.losses, 
                th.draws, 
                th.championships,
                p.id AS player_id,
                p.name AS player_name,
                p.position AS player_position,
                p.player_image_url AS player_image
            FROM teams t
            LEFT JOIN team_season_history th ON t.id = th.team_id
            LEFT JOIN team_player_mapping tp ON t.id = tp.team_id
            LEFT JOIN players p ON tp.player_id = p.id
            WHERE t.id = %s
        """
        
        with self.db_connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
            cursor.execute(query, (team_id,))
            team_details = cursor.fetchall()
        
        return team_details
