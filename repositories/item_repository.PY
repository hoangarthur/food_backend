# repositories/item_repository.py
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text

class ItemRepository:
    """Repository for item-related database operations"""

    def __init__(self, session: AsyncSession):
        self.session = session

    def get_item_by_id(self, item_id: int):
        """Fetch an item by its ID"""
        result = self.session.execute(
            text("SELECT * FROM items WHERE id = :item_id"),
            {"item_id": item_id}
        )
        return result.mappings().first()  # return dict or None

    def get_items_by_name(self, name: str):
        """Fetch items by their name"""
        result = self.session.execute(
            text("SELECT * FROM items WHERE name = :name"),
            {"name": name}
        )
        return result.mappings().all()  # return list of dicts

    def get_items_by_user(self, user_id: int):
        """Fetch all items for a specific user"""
        result = self.session.execute(
            text("SELECT * FROM items WHERE user_id = :user_id"),
            {"user_id": user_id}
        )
        return result.mappings().all()

    def get_items_by_receipt_id(self, receipt_id: int):
        """Fetch items by receipt ID"""
        result = self.session.execute(
            text("SELECT * FROM items WHERE receiptId = :receipt_id"),
            {"receipt_id": receipt_id}
        )
        return result.mappings().all()

    def check_item_exists(self, item_id: int) -> bool:
        """Check if an item exists by ID"""
        result = self.session.execute(
            text("SELECT COUNT(*) as count FROM items WHERE id = :item_id"),
            {"item_id": item_id}
        )
        return result.scalar() > 0 

    def create_item(self, name: str, price: float, quantity: int, date: str, 
                          store: str, category: str, receipt_id: int) -> int:
        """Create a new item and return new item_id"""
        result = self.session.execute(
            text("""
                INSERT INTO items (name, price, quantity, date, store, category, receiptId) 
                VALUES (:name, :price, :quantity, :date, :store, :category, :receipt_id)
            """),
            {"name": name, "price": price, "quantity": quantity, "date": date,
             "store": store, "category": category, "receipt_id": receipt_id}
        )
        self.session.commit()
        return result.lastrowid  # return int 

    def update_item(self, updated_data: dict) -> bool:
        """Update an item's details and return True if successful"""
        item_id = updated_data['item_id']
        name = updated_data.get('name')
        price = updated_data.get('price')
        quantity = updated_data.get('quantity')
        store = updated_data.get('store')
        category = updated_data.get('category')
        date = updated_data.get('date')

        result = self.session.execute(
            text("""
                UPDATE items 
                SET name = COALESCE(:name, name),
                    price = COALESCE(:price, price),
                    quantity = COALESCE(:quantity, quantity),
                    date = COALESCE(:date, date),
                    store = COALESCE(:store, store),
                    category = COALESCE(:category, category)
                WHERE id = :item_id
            """),
            {
                "name": name, "price": price, "quantity": quantity, "date": date,
                "store": store, "category": category, "item_id": item_id
            }
        )
        self.session.commit()
        return result.rowcount > 0  # return bool

    def delete_item_by_item_id(self, item_id: int) -> bool:
        """Delete an item by ID and return True if successful"""
        result = self.session.execute(
            text("DELETE FROM items WHERE id = :item_id"),
            {"item_id": item_id}
        )
        self.session.commit()
        return result.rowcount > 0