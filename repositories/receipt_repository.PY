# repositories/receipt_repository.py
from core.database import get_db_connection
from repositories.item_repository import ItemRepository

class ReceiptRepository:
    """Repository for receipt-related database operations"""
    def get_receipt_by_id(self, receipt_id):
        """Fetch a receipt by its ID"""
        with get_db_connection() as conn:
            cursor = conn.cursor(dictionary=True)
            query = "SELECT * FROM receipts WHERE id = %s"
            cursor.execute(query, (receipt_id,))
            receipt = cursor.fetchone()
            cursor.close()
            return receipt

    def get_receipts_by_user(self, user_id):
        """Fetch all receipts for a specific user"""
        with get_db_connection() as conn:
            cursor = conn.cursor(dictionary=True)
            query = "SELECT * FROM receipts WHERE user_id = %s"
            cursor.execute(query, (user_id,))
            receipts = cursor.fetchall()
            cursor.close()
            return receipts
    
    def check_receipt_exists(self, receipt_id):
        """Check if a receipt exists by ID"""
        with get_db_connection() as conn:
            cursor = conn.cursor(dictionary=True)
            query = "SELECT COUNT(*) as count FROM receipts WHERE id = %s"
            cursor.execute(query, (receipt_id))
            result = cursor.fetchone()
            cursor.close()
            return result['count'] > 0

    # added method
    def create_receipt(self, receipt_id, user_id, item):
        """Create a new receipt and associated items"""
        with get_db_connection() as conn:
            cursor = conn.cursor()
            query = "INSERT INTO receipts (id, user_id) VALUES (%s, %s)"
            cursor.execute(query, (receipt_id, user_id))
            conn.commit()
            cursor.close()
        item_repo = ItemRepository()
        for it in item:
            item_repo.create_item(it['name'], it['price']) 
        return receipt_id