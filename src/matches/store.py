from db.connection import get_db_connection
from datetime import datetime
from typing import List, Dict, Optional

class MatchesStore:
    def __init__(self, db_connection=None):
        self.db_connection = db_connection or get_db_connection()

    def get_filtered_matches(self, date: Optional[str] = None, status: Optional[str] = None, season: Optional[str] = None, team_name: Optional[str] = None) -> List[Dict]:
        query = """
            SELECT 
                matches.id,
                matches.team1_id,
                team1.name AS team1_name,
                team1.logo_url AS team1_logo_url,
                matches.team2_id,
                team2.name AS team2_name,
                team2.logo_url AS team2_logo_url,
                matches.match_datetime,
                matches.location,
                matches.country,
                matches.season,
                matches.status,
                matches.league_id,
                leagues.name AS league_name,
                leagues.icon_url AS league_icon_url,
                matches.score_team1,
                matches.score_team2,
                matches.winner_id,
                winner.name AS winner_name,
                winner.logo_url AS winner_logo_url
            FROM matches
            LEFT JOIN teams AS team1 ON matches.team1_id = team1.id
            LEFT JOIN teams AS team2 ON matches.team2_id = team2.id
            LEFT JOIN leagues ON matches.league_id = leagues.id
            LEFT JOIN teams AS winner ON matches.winner_id = winner.id
        """

        filters = []
        if status is None or status.lower() != "all":
            if date:
                filters.append(f"DATE(matches.match_datetime) = '{datetime.fromisoformat(date).date()}'")
            if status:
                filters.append(f"LOWER(matches.status) = LOWER('{status}')")
            if season:
                filters.append(f"LOWER(matches.season) = LOWER('{season}')")
            if team_name:
                filters.append(f"(LOWER(team1.name) = LOWER('{team_name}') OR LOWER(team2.name) = LOWER('{team_name}'))")
        
        if filters:
            query += " WHERE " + " AND ".join(filters)

        with self.db_connection.cursor() as cursor:
            cursor.execute(query)
            matches = cursor.fetchall()
        
        return matches
