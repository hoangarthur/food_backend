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
    def create_receipt(self, user_id, items):
        """Create a new receipt and associated items"""
        with get_db_connection() as conn:
            cursor = conn.cursor()
            try:
                conn.start_transaction()
                # Insert receipt
                cursor.execute(
                    "INSERT INTO receipts (userId, date, source, status) VALUES (%s, %s, %s, %s)",
                    (user_id, items[0]['date'], "default_source", "default_status")
                )
                receipt_id = cursor.lastrowid

                # Insert all items
                insert_item_query = """
                    INSERT INTO items (name, price, quantity, date, store, category, receiptId)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                """
                for item in items:
                    cursor.execute(insert_item_query, (
                        item['name'], item['price'], item['quantity'],
                        item['date'], item['store'], item['category'], receipt_id
                ))
                conn.commit()
                return receipt_id
            except Exception as e:
                conn.rollback()
                raise e

    def update_receipt(self,updated_data):
        """Update a receipt and its associated items"""
        receipt_id = updated_data['receiptId']
        items = updated_data['items']
        with get_db_connection() as conn:
            # Check if receipt exists
            receipt = self.get_receipt_by_id(receipt_id)
            if not receipt:
                receipt_id = self.create_receipt(updated_data.get('userId'), updated_data.get('items', []))
                return receipt_id
                #Todo: return http response indicating creation
            else:
                new_receipt_source = updated_data.get('source')
                new_receipt_status = updated_data.get('status') 
                cursor = conn.cursor()
                query = "UPDATE receipts SET source = %s, status = %s WHERE receiptId = %s"
                cursor.execute(query, (new_receipt_source, new_receipt_status, receipt_id,))

                # Update associated items if provided
                cursor.execute("DELETE FROM items WHERE receiptId = %s", (receipt_id,))
                
                # Insert all items
                insert_item_query = """
                    INSERT INTO items (name, price, quantity, date, store, category, receiptId)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                """
                for item in items:
                    cursor.execute(insert_item_query, (
                        item['name'], item['price'], item['quantity'],
                        item['date'], item['store'], item['category'], receipt_id
                ))
                conn.commit()
                 #Todo: return http response indicating creation
    
    def delete_receipt_by_id(self, receipt_id):
        if receipt_id is None:
            return False
        """Delete a receipt by ID"""
        with get_db_connection() as conn:
            cursor = conn.cursor()
            query = "DELETE FROM receipts WHERE receiptId = %s"
            cursor.execute(query, (receipt_id,))
            conn.commit()
            return cursor.rowcount > 0