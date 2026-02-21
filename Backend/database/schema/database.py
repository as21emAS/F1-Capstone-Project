# scripts/database.py
import psycopg2
from psycopg2 import pool

class Database:
    _connection_pool = None
    
    @classmethod
    def initialize(cls, minconn=1, maxconn=10):
        cls._connection_pool = psycopg2.pool.SimpleConnectionPool(
            minconn,
            maxconn,
            dbname="f1_predictor",
            user="your_username",
            password="your_password",
            host="localhost",
            port="5432"
        )
    
    @classmethod
    def get_connection(cls):
        return cls._connection_pool.getconn()
    
    @classmethod
    def return_connection(cls, connection):
        cls._connection_pool.putconn(connection)