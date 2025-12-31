# core/database.py
import mysql.connector
from contextlib import contextmanager
from mysql.connector import Error

DB_CONFIG = {
    'host': 'localhost',         
    'user': 'root',             
    'password': '122442',  
    'database': 'FoodSQL'
}
@contextmanager
def get_db_connection():
    """Get a MySQL connection using context manager"""
    conn = None
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        if conn.is_connected():
            print("Database connection established")
            yield conn
        else:
            raise ConnectionError("Failed to connect to the database")
    except Error as e:
        print(f"Database error: {e}")
        raise
    finally:
        if conn.is_connected():
            print("Closing database connection")
            conn.close()

def get_db_cursor():
    """Quick way to get cursor"""
    with get_db_connection() as conn:
        yield conn.cursor(dictionary=True) 