import os
from psycopg2 import pool
from dotenv import load_dotenv

load_dotenv()

# Connection pool configuration
DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://livreiter:@localhost:5432/f1_predictor')
POOL_SIZE = int(os.getenv('DATABASE_POOL_SIZE', 10))
MAX_OVERFLOW = int(os.getenv('DATABASE_MAX_OVERFLOW', 20))

# Create connection pool
connection_pool = None

def initialize_pool():
    """Initialize the database connection pool"""
    global connection_pool
    
    if connection_pool is None:
        connection_pool = pool.ThreadedConnectionPool(
            minconn=1,
            maxconn=POOL_SIZE,
            dsn=DATABASE_URL
        )
        print(f"✓ Connection pool initialized (size: {POOL_SIZE})")
    
    return connection_pool

def get_connection():
    """Get a connection from the pool"""
    if connection_pool is None:
        initialize_pool()
    
    return connection_pool.getconn()

def return_connection(conn):
    """Return a connection to the pool"""
    if connection_pool:
        connection_pool.putconn(conn)

def close_all_connections():
    """Close all connections in the pool"""
    global connection_pool
    if connection_pool:
        connection_pool.closeall()
        connection_pool = None
        print("✓ All connections closed")
