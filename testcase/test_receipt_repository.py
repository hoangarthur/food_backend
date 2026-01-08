import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import json
import pytest
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from repositories import UserRepository, RecipeRepository, ItemRepository, ReceiptRepository

# Synchronous engine + session
engine = create_engine("sqlite:///:memory:", echo=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def session():
    session = SessionLocal()
    
    # Luôn drop tất cả trước khi create (để tránh bảng cũ không có cascade)
    session.execute(text("DROP TABLE IF EXISTS items"))
    session.execute(text("DROP TABLE IF EXISTS receipts"))
    session.execute(text("DROP TABLE IF EXISTS recipes"))
    session.execute(text("DROP TABLE IF EXISTS users"))
    
    # Tạo users trước (parent)
    session.execute(text("""
        CREATE TABLE users (
            userId INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """))
    
    # Tạo receipts với CASCADE rõ ràng
    session.execute(text("""
        CREATE TABLE receipts (
            receiptId INTEGER PRIMARY KEY AUTOINCREMENT,
            userId INTEGER NOT NULL,
            source TEXT,
            status TEXT,
            date DATE,
            FOREIGN KEY (userId) REFERENCES users(userId) ON DELETE CASCADE
        )
    """))
    
    # Tạo items với CASCADE
    session.execute(text("""
        CREATE TABLE items (
            itemId INTEGER PRIMARY KEY AUTOINCREMENT,
            receiptId INTEGER NOT NULL,
            name TEXT,
            price REAL,
            quantity INTEGER,
            date DATE,
            store TEXT,
            category TEXT,
            FOREIGN KEY (receiptId) REFERENCES receipts(receiptId) ON DELETE CASCADE
        )
    """))
    
    # Tạo recipes nếu cần (cũng có CASCADE)
    session.execute(text("""
        CREATE TABLE recipes (
            recipeId INTEGER PRIMARY KEY AUTOINCREMENT,
            userId INTEGER NOT NULL,
            title TEXT,
            description TEXT,
            ingredients TEXT,
            instructions TEXT,
            source TEXT,
            nutrition INTEGER,
            totalTime INTEGER,
            dateSaved DATE,
            servings INTEGER,
            FOREIGN KEY (userId) REFERENCES users(userId) ON DELETE CASCADE
        )
    """))
    
    session.commit()
    yield session
    session.close()


userDb = {
    "user_id": None,
    "email": "example@gmail.com",
    "password": "examplepassword",
    "new_email": "newexample@gmail.com",
    "new_password": "newexamplepassword"
}

receipt = {
    "receipt_id": None
}

items = [
    {
    "name": "Sample Item 1",
    "price": 10.99,
    "quantity": 2,
    "date": "2024-01-01",
    "store": "Sample Store",
    "category": "Sample Category"
    },
    {
    "name": "Sample Item 2",
    "price": 11.99,
    "quantity": 5,
    "date": "2024-01-01",
    "store": "Sample Store 2",
    "category": "Sample Category 2"
    }
    ]

#add new user to database
def test_receipt(session):
    global userDb, receipt, items
    User_Repo = UserRepository(session)
    Receipt_Repo = ReceiptRepository(session)
    Item_Repo = ItemRepository(session)
    
    email = userDb["email"]
    password = userDb["password"]
    userDb['user_id'] = User_Repo.get_userId_by_email(email,)
    if userDb['user_id'] is not None:
        User_Repo.delete_user(email,)
        session.commit()
    userID = User_Repo.create_user(email, password)
    session.commit()
    userDb['user_id'] = userID
    assert userID is not None, "Failed to create user"
    
    #create new receipt for user
    user_id = userDb["user_id"]
    receipt_id = Receipt_Repo.create_receipt(user_id, items)
    session.commit()
    receipt["receipt_id"] = receipt_id
    receipts = Receipt_Repo.get_receipt_by_id(receipt_id,)
    assert receipts is not None, "Failed to create receipt"
    
    #verify items added to receipt
    receipt_id = receipt.get("receipt_id")
    receipts = Receipt_Repo.get_receipt_by_id(receipt_id,)
    items = Item_Repo.get_items_by_receipt_id(receipt_id,)
    if receipts is None:
        pytest.skip("Receipt does not exist")
        
    # verify items associated with the receipt
    assert len(items) == 2, "Receipt should contain 2 items"
    assert items[0]["name"] == "Sample Item 1", "First item name does not match"
    assert items[1]["name"] == "Sample Item 2", "Second item name does not match"
    
    #test update receipt
    receipt_id = receipt.get("receipt_id")
    updated_data = {
        "receiptId": receipt_id,
        "source": "Updated Source",
        "status": "Updated Status",
        "items": [
            {
                "name": "Updated Item 1",
                "price": 12.99,
                "quantity": 3,
                "date": "2024-02-01",
                "store": "Updated Store",
                "category": "Updated Category"
            }
        ]
    }
    Receipt_Repo.update_receipt(updated_data)
    items = Item_Repo.get_items_by_receipt_id(receipt_id,)
    receipts = Receipt_Repo.get_receipt_by_id(receipt_id)
    assert items is not None, "Receipt should exist after update"
    assert receipts["source"] == "Updated Source", "Receipt source was not updated"
    assert receipts["status"] == "Updated Status", "Receipt status was not updated"
    assert len(items) == 1, "Receipt should contain 1 updated item"
    assert items[0]["name"] == "Updated Item 1", "Updated item name does not match"

    #delete receipt, user from database by id
    email = userDb['email']
    success = User_Repo.delete_user(email,)
    session.commit()
    assert success is True, "Delete user failed"
    success = Receipt_Repo.delete_receipt_by_id(receipt_id,)
    session.commit()
    assert success is True, "Delete receipt failed"

    #verify delete
    user = User_Repo.get_user_by_id(userDb["user_id"],)
    assert user is None, "User should be None after deletion"
    
    #verify receipt delete cascade
    receipt_id = receipt["receipt_id"]
    receipts = Receipt_Repo.get_receipt_by_id(receipt_id,)
    assert receipts is None, "Receipt should be None after user deletion"
    
    