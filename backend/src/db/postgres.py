import psycopg2
from psycopg2.extras import RealDictCursor
import os
from urllib.parse import urlparse

def get_postgres_cursor():
    # Retrieve the PostgreSQL connection string
    postgres_url = os.getenv("POSTGRES_URL")
    
    # Parse the connection string
    if postgres_url:
        result = urlparse(postgres_url)
        username = result.username
        password = result.password
        database = result.path[1:]
        hostname = result.hostname
        port = result.port
    else:
        # Fallback values for local development
        hostname = os.getenv("POSTGRES_HOST", "localhost")
        database = os.getenv("POSTGRES_DB", "halal_db")
        username = os.getenv("POSTGRES_USER", "postgres")
        password = os.getenv("POSTGRES_PASSWORD", "postgres")
        port = 5432

    # Establish a connection to PostgreSQL
    conn = psycopg2.connect(
        host=hostname,
        database=database,
        user=username,
        password=password,
        port=port
    )
    
    return conn.cursor(cursor_factory=RealDictCursor)
