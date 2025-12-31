import mysql.connector
from mysql.connector import Error


try:
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="122442",
        database="FoodSQL"
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
        
