# repositories/receipt_repository.py
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from typing import List, Dict, Any

class ReceiptRepository:
    """Repository for receipt-related database operations"""

    def __init__(self, session: AsyncSession):
        self.session = session

    def get_receipt_by_id(self, receipt_id: int) -> Dict[str, Any] | None:
        """Fetch a receipt by its ID"""
        result = self.session.execute(
            text("SELECT * FROM receipts WHERE receiptId = :receipt_id"),
            {"receipt_id": receipt_id}
        )
        return result.mappings().first()  # return dict or None

    def get_receipts_by_user(self, user_id: int) -> List[Dict[str, Any]]:
        """Fetch all receipts for a specific user"""
        result = self.session.execute(
            text("SELECT * FROM receipts WHERE userId = :user_id"),
            {"user_id": user_id}
        )
        return result.mappings().all()  # return list of dicts

    def create_receipt(self, user_id: int, items: List[Dict[str, Any]]) -> int:
        """Create a new receipt and associated items, return new receipt_id"""
        if not items:
            raise ValueError("Items list cannot be empty")

        with self.session.begin():  # tự động rollback nếu lỗi
            # Insert receipt
            result = self.session.execute(
                text("""
                    INSERT INTO receipts (userId, date, source, status) 
                    VALUES (:user_id, :date, :source, :status)
                """),
                {
                    "user_id": user_id,
                    "date": items[0]["date"],
                    "source": "default_source",
                    "status": "default_status"
                }
            )
            receipt_id = result.lastrowid

            # Insert all items
            for item in items:
                self.session.execute(
                    text("""
                        INSERT INTO items (name, price, quantity, date, store, category, receiptId)
                        VALUES (:name, :price, :quantity, :date, :store, :category, :receipt_id)
                    """),
                    {
                        "name": item["name"],
                        "price": item["price"],
                        "quantity": item["quantity"],
                        "date": item["date"],
                        "store": item["store"],
                        "category": item["category"],
                        "receipt_id": receipt_id
                    }
                )

        return receipt_id

    def update_receipt(self, updated_data: Dict[str, Any]) -> int:
        """Update a receipt and its associated items, return receipt_id (create new if not exist)"""
        receipt_id = updated_data.get("receiptId")
        items = updated_data.get("items", [])

        if not receipt_id:
            # If no receipt_id provided, create a new receipt
            return self.create_receipt(
                updated_data.get("userId"),
                items
            )

        receipt = self.get_receipt_by_id(receipt_id)
        if not receipt:
            return self.create_receipt(
                updated_data.get("userId"),
                items
            )

        # Update receipt info
        self.session.execute(
            text("""
                UPDATE receipts 
                SET source = COALESCE(:source, source),
                    status = COALESCE(:status, status)
                WHERE receiptId = :receipt_id
            """),
            {
                "source": updated_data.get("source"),
                "status": updated_data.get("status"),
                "receipt_id": receipt_id
            }
        )
        # Delete existing items for the receipt
        self.session.execute(
            text("DELETE FROM items WHERE receiptId = :receipt_id"),
            {"receipt_id": receipt_id}
        )
        # Insert items 
        for item in items:
            self.session.execute(
                text("""
                    INSERT INTO items (name, price, quantity, date, store, category, receiptId)
                    VALUES (:name, :price, :quantity, :date, :store, :category, :receipt_id)
                """),
                {
                    "name": item["name"],
                    "price": item["price"],
                    "quantity": item["quantity"],
                    "date": item["date"],
                    "store": item["store"],
                    "category": item["category"],
                    "receipt_id": receipt_id
                }
            )
        return receipt_id

    def delete_receipt_by_id(self, receipt_id: int | None) -> bool:
        """Delete a receipt by ID and return True if successful"""
        if receipt_id is None:
            return False

        result = self.session.execute(
            text("DELETE FROM receipts WHERE receiptId = :receipt_id"),
            {"receipt_id": receipt_id}
        )
        self.session.commit()
        return result.rowcount > 0