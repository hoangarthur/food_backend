import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from repositories import ReceiptRepository, UserRepository, ItemRepository
import pytest
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
def test_create_user():
    email = userDb["email"]
    password = userDb["password"]
    userDb['user_id'] = UserRepository().get_userId_by_email(email)
    if userDb['user_id'] is not None:
        pytest.skip("User with this email already exists")
    userID = UserRepository().create_user(email, password)
    userDb['user_id'] = userID
    assert userID is not None, "Failed to create user"

def test_create_new_receipt():
    user_id = userDb["user_id"]
    receipt_id = ReceiptRepository().create_receipt(user_id, items)
    receipt["receipt_id"] = receipt_id
    receipts = ReceiptRepository().get_receipt_by_id(receipt_id)
    assert receipts is not None, "Failed to create receipt"

def test_receipt_contains_items():
    receipt_id = receipt.get("receipt_id")
    receipts = ReceiptRepository().get_receipt_by_id(receipt_id)
    items = ItemRepository().get_items_by_receipt_id(receipt_id)
    if receipts is None:
        pytest.skip("Receipt does not exist")
    # verify items associated with the receipt
    assert len(items) == 2, "Receipt should contain 2 items"
    assert items[0]["name"] == "Sample Item 1", "First item name does not match"
    assert items[1]["name"] == "Sample Item 2", "Second item name does not match"

def test_update_receipt():
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
    ReceiptRepository().update_receipt(updated_data)
    items = ItemRepository().get_items_by_receipt_id(receipt_id)
    receipts = ReceiptRepository().get_receipt_by_id(receipt_id)
    assert items is not None, "Receipt should exist after update"
    assert receipts["source"] == "Updated Source", "Receipt source was not updated"
    assert receipts["status"] == "Updated Status", "Receipt status was not updated"
    assert len(items) == 1, "Receipt should contain 1 updated item"
    assert items[0]["name"] == "Updated Item 1", "Updated item name does not match"

#delete user from database by id
def test_delete_user_from_db():
    email = userDb['email']
    success = UserRepository().delete_user(email,)
    assert success is True, "Delete user failed"
    #verify delete
    user = UserRepository().get_user_by_id(userDb["user_id"],)
    assert user is None, "User should be None safter deletion"
    
def test_delete_receipt():
    receipt_id = receipt["receipt_id"]
    receipts = ReceiptRepository().get_receipt_by_id(receipt_id)
    assert receipts is None, "Receipt should be None after user deletion"
    
    