# repositories/user_repository.py
from core.database import get_db_connection

class UserRepository:
    """Repository for user-related database operations"""

    def get_user_by_id(self, user_id):
        """Fetch a user by their ID"""
        with get_db_connection() as conn:
            cursor = conn.cursor(dictionary=True)
            query = "SELECT * FROM users WHERE id = %s"
            cursor.execute(query, (user_id))
            user = cursor.fetchone()
            cursor.close()
            return user
        
    def check_user_exists(self, email):
        """Check if a user exists by email"""
        with get_db_connection() as conn:
            cursor = conn.cursor(dictionary=True)
            query = "SELECT COUNT(*) as count FROM users WHERE email = %s"
            cursor.execute(query, (email))
            result = cursor.fetchone()
            cursor.close()
            return result['count'] > 0
    
    def create_user(self, username, email):
        """Create a new user"""
        with get_db_connection() as conn:
            cursor = conn.cursor()
            query = "INSERT INTO users (username, email) VALUES (%s, %s)"
            cursor.execute(query, (username, email))
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
            cursor.exercute(query, (email))
            conn.commit()
            cursor.close()
            return cursor.rowcount > 0
