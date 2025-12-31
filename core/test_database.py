
from database import get_db_connection
from mysql.connector import Error

try:
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SHOW TABLES")
        print("Tables in the database:")
        for table in cursor.fetchall():
            print(table)
except Error as e:
    print(f"Error while connecting to MySQL: {e}")
finally:
    print("MySQL connection is closed")