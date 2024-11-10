import psycopg2
from psycopg2.extras import RealDictCursor
from config.config import Config
from urllib.parse import urlparse

def get_db_connection():
    db_url = urlparse(Config.SQLALCHEMY_DATABASE_URI)
    
    db_name = db_url.path[1:]  
    db_user = db_url.username
    db_password = db_url.password
    db_host = db_url.hostname
    db_port = db_url.port

    conn = psycopg2.connect(
        dbname=db_name,
        user=db_user,
        password=db_password,
        host=db_host,
        port=db_port,
        cursor_factory=RealDictCursor
    )
    
    return conn
