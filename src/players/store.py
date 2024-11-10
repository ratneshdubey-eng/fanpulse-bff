from db.connection import get_db_connection
from typing import List, Dict, Optional
import psycopg2.extras

class PlayersStore:
    def __init__(self, db_connection=None):
        self.db_connection = db_connection or get_db_connection()

    def get_all_players(self) -> List[Dict]:
        query = """
            SELECT id, name, position, jersey_number, player_image_url
            FROM players
        """
        with self.db_connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
            cursor.execute(query)
            players = cursor.fetchall()
        return players

    def get_player_by_id(self, player_id: str) -> Optional[Dict]:
        query = """
            SELECT p.id, p.name, p.position, p.jersey_number, p.team_id, p.player_image_url,
                   pd.date_of_birth, pd.height_cm, pd.weight_kg,
                   c.name AS country_name,
                   ps.games_played, ps.minutes_per_game, ps.field_goal_percentage,
                   ps.three_point_percentage, ps.free_throw_percentage,
                   ps.rebounds_per_game, ps.assists_per_game, ps.blocks_per_game,
                   ps.steals_per_game, ps.personal_fouls_per_game, ps.turnovers_per_game, ps.points_per_game,
                   sm.twitter, sm.instagram, sm.facebook, sm.youtube
            FROM players p
            LEFT JOIN player_details pd ON p.id = pd.player_id
            LEFT JOIN countries c ON pd.country_id = c.id
            LEFT JOIN player_stats ps ON pd.stats_id = ps.id
            LEFT JOIN social_media sm ON pd.social_media_id = sm.id
            WHERE p.id = %s
        """
        with self.db_connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
            cursor.execute(query, (player_id,))
            player = cursor.fetchone()
        return player
