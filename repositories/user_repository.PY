# repositories/user_repository.py
from core.database import get_db_connection

class UserRepository:
    """Repository for user-related database operations"""

    def get_user_by_id(self, user_id):
        """Fetch a user by their ID"""
        with get_db_connection() as conn:
            cursor = conn.cursor(dictionary=True)
            query = "SELECT * FROM users WHERE userId = %s"
            cursor.execute(query, (user_id,))
            user = cursor.fetchone()
            cursor.close()
            return user
    def get_userId_by_email(self, email):
        """Fetch a user's ID by their email"""
        with get_db_connection() as conn:
            cursor = conn.cursor()
            query = "SELECT userId FROM users WHERE email = %s"
            cursor.execute(query, (email,))
            result = cursor.fetchone()
            cursor.close()
            return result[0] if result else None
        
    def check_user_exists(self, email):
        """Check if a user exists by email"""
        with get_db_connection() as conn:
            cursor = conn.cursor(dictionary=True)
            query = "SELECT COUNT(*) as count FROM users WHERE email = %s"
            cursor.execute(query, (email,))
            result = cursor.fetchone()
            cursor.close()
            return result['count'] > 0
    
    def create_user(self, email, password):
        #check user exists
        if self.check_user_exists(email,):
            raise Exception("User with this email already exists")
        """Create a new user"""
        with get_db_connection() as conn:
            cursor = conn.cursor()
            query = "INSERT INTO users (email, password) VALUES (%s, %s)"
            cursor.execute(query, (email, password))
            conn.commit()
            user_id = cursor.lastrowid
            cursor.close()
            return user_id
        
    def update_user_password(self, email, new_password):
        """Update a user's password"""
        with get_db_connection() as conn:
            cursor = conn.cursor()
            query = "UPDATE users SET password = %s WHERE email = %s"
            cursor.execute(query, (new_password, email))
            conn.commit()
            cursor.close()
            return cursor.rowcount > 0
        
    def delete_user(self, email):
        """delete a user by email"""
        with get_db_connection() as conn:
            cursor = conn.cursor()
            query = "DELETE FROM users WHERE email = %s"
            cursor.execute(query, (email,))
            conn.commit()
            cursor.close()
            return cursor.rowcount > 0
    