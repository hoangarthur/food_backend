import mysql.connector
from mysql.connector import Error
from config import DB_CONFIG

try:
    conn = mysql.connector.connect(
        host=DB_CONFIG['host'],
        user=DB_CONFIG['user'],
        password=DB_CONFIG['password'],
        database=DB_CONFIG['database']
    )
    
    if conn.is_connected():
        print("connected to mysql database")
        
        cursor = conn.cursor()
        cursor.execute("SHOW TABLES")
        print("Tables in the database:")
        for table in cursor.fetchall():
            print(table)
except Error as e:
    print(f"Error while connecting to MySQL: {e}")
finally:
    if conn.is_connected():
        cursor.close()
        conn.close()
        print("MySQL connection is closed")
        
