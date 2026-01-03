# repositories/receipt_repository.py
from repositories.item_repository import ItemRepository
from core.database import get_db_connection

class ReceiptRepository:
    """Repository for receipt-related database operations"""
    def get_receipt_by_id(self, receipt_id):
        """Fetch a receipt by its ID"""
        with get_db_connection() as conn:
            cursor = conn.cursor(dictionary=True)
            query = "SELECT * FROM receipts WHERE receiptId = %s"
            cursor.execute(query, (receipt_id,))
            receipt = cursor.fetchone()
            return receipt

    def get_receipts_by_user(self, user_id):
        """Fetch all receipts for a specific user"""
        with get_db_connection() as conn:
            cursor = conn.cursor(dictionary=True)
            query = "SELECT * FROM receipts WHERE userId = %s"
            cursor.execute(query, (user_id,))
            receipts = cursor.fetchall()
            return receipts
    
    # added method
    def create_receipt(self, receipt_id, user_id, item):
        """Create a new receipt and associated items"""
        with get_db_connection() as conn:
            cursor = conn.cursor()
            query = "INSERT INTO receipts (receiptId, userId) VALUES (%s, %s)"
            cursor.execute(query, (receipt_id, user_id))
            conn.commit()
        item_repo = ItemRepository()
        for it in item:
            item_repo.create_item(it['name'], it['price'], it['quantity'], it['date'], it['store'], it['category'], receipt_id)
         #Todo: return http response indicating creation

    def update_receipt(self,updated_data):
        """Update a receipt and its associated items"""
        receipt_id = updated_data['receipt_id']
        items = updated_data.get('items', [])
        with get_db_connection() as conn:
            # Check if receipt exists
            cursor = conn.cursor(dictionary=True)
            query = "SELECT * FROM receipts WHERE receiptId = %s"
            cursor.execute(query, (updated_data['receiptId'],))
            receipt = cursor.fetchone()
            if not receipt:
                create_receipt = self.create_receipt(updated_data['receiptId'], updated_data.get('userId'), updated_data.get('items', []))
                #Todo: return http response indicating creation
            else:
                new_receipt_source = updated_data.get('source')
                new_receipt_status = updated_data.get('status') 
                cursor = conn.cursor()
                query = "UPDATE receipts SET source = %s, status = %s WHERE receiptId = %s"
                cursor.execute(query, (new_receipt_source, new_receipt_status, receipt_id,))

                # Update associated items if provided
                cursor.execute("DELETE FROM items WHERE receipt_id = %s", (receipt_id,))
                item_repo = ItemRepository()
                for it in items:
                    item_repo.create_item(it['name'], it['price'], it['quantity'],it['date'],it['store'],it['category'], receipt_id)
                conn.commit()
                 #Todo: return http response indicating creation
    
    def delete_receipt_by_id(self, receipt_id):
        """Delete a receipt by ID"""
        with get_db_connection() as conn:
            cursor = conn.cursor()
            query = "DELETE FROM receipts WHERE receiptId = %s"
            cursor.execute(query, (receipt_id,))
            conn.commit()
            return cursor.rowcount > 0