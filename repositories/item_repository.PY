# repositories/user_repository.py
from core.database import get_db_connection

class ItemRepository:
    """Repository for item-related database operations"""
    def get_item_by_id(self, item_id):
        """Fetch an item by its ID"""
        with get_db_connection() as conn:
            cursor = conn.cursor(dictionary=True)
            query = "SELECT * FROM items WHERE id = %s"
            cursor.execute(query, (item_id,))
            item = cursor.fetchone()
            return item
        
    def get_items_by_name(self, name):
        """Fetch items by their name"""
        with get_db_connection() as conn:
            cursor = conn.cursor(dictionary=True)
            query = "SELECT * FROM items WHERE name = %s"
            cursor.execute(query, (name,))
            items = cursor.fetchall()
            return items

    def get_items_by_user(self, user_id):
        """Fetch all items for a specific user"""
        with get_db_connection() as conn:
            cursor = conn.cursor(dictionary=True)
            query = "SELECT * FROM items WHERE user_id = %s"
            cursor.execute(query, (user_id,))
            items = cursor.fetchall()
            return items

    def get_items_by_receipt(self, receipt_id):
        """Fetch items by receipt ID"""
        with get_db_connection() as conn:
            cursor = conn.cursor(dictionary=True)
            query = "SELECT * FROM items WHERE receipt_id = %s"
            cursor.execute(query, (receipt_id,))
            items = cursor.fetchall()
            return items
    
    def check_item_exists(self, item_id):
        """Check if an item exists by ID"""
        with get_db_connection() as conn:
            cursor = conn.cursor(dictionary=True)
            query = "SELECT COUNT(*) as count FROM items WHERE id = %s"
            cursor.execute(query, (item_id,))
            result = cursor.fetchone()
            return result['count'] > 0

    def create_item(self, name, price, quantity, date, store, category, receipt_id):
        """Create a new item"""
        with get_db_connection() as conn:
            cursor = conn.cursor()
            query = "INSERT INTO items (name, price, quantity, date, store, category, receipt_id) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            cursor.execute(query, (name, price, quantity, date, store, category, receipt_id))
            conn.commit()
            item_id = cursor.lastrowid
            return item_id

    def update_item_price(self, item_id, new_price):
        """Update an item's price"""
        with get_db_connection() as conn:
            cursor = conn.cursor()
            query = "UPDATE items SET price = %s WHERE id = %s"
            cursor.execute(query, (new_price, item_id,))
            conn.commit()
            return cursor.rowcount > 0

    def delete_item_by_item_id(self, item_id):
        """delete an item by ID"""
        with get_db_connection() as conn:
            cursor = conn.cursor()
            query = "DELETE FROM items WHERE id = %s"
            cursor.execute(query, (item_id,))
            conn.commit()
            return cursor.rowcount > 0
