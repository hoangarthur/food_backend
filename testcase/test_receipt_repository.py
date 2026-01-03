import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from repositories import ReceiptRepository, UserRepository
import pytest
user = {
    "user_id": None,
    "email": "example@gmail.com",
    "password": "examplepassword",
    "new_email": "newexample@gmail.com",
    "new_password": "newexamplepassword"
}

receipt = {
    "receipt_id": "receipt_123"
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
    email = user["email"]
    password = user["password"]
    userID = UserRepository().create_user(email, password)
    user['user_id'] = userID
    assert userID is not None, "Failed to create user"

def test_create_new_receipt():
    receipt_id = receipt["receipt_id"]
    user_id = user["user_id"]
    ReceiptRepository().create_receipt(receipt_id, user_id, items)
    receipt = ReceiptRepository().get_receipt_by_id(receipt_id)
    assert receipt is not None, "Failed to create receipt"
    assert receipt["id"] == receipt_id, "Receipt ID does not match"
    
def test_receipt_contains_items():
    receipt_id = receipt["receipt_id"]
    receipt = ReceiptRepository().get_receipt_by_id(receipt_id)
    assert receipt is not None, "Receipt should exist"
    # Further logic can be added to verify items associated with the receipt
    assert len(receipt["items"]) == 2, "Receipt should contain 2 items"
    assert receipt["items"][0]["name"] == "Sample Item 1", "First item name does not match"
    assert receipt["items"][1]["name"] == "Sample Item 2", "Second item name does not match"

def test_update_receipt():
    receipt_id = receipt["receipt_id"]
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
    receipt = ReceiptRepository().get_receipt_by_id(receipt_id)
    assert receipt is not None, "Receipt should exist after update"
    assert receipt["source"] == "Updated Source", "Receipt source was not updated"
    assert receipt["status"] == "Updated Status", "Receipt status was not updated"
    assert len(receipt["items"]) == 1, "Receipt should contain 1 updated item"
    assert receipt["items"][0]["name"] == "Updated Item 1", "Updated item name does not match"

#delete user from database by id
def test_delete_user_from_db():
    email = user['email']
    success = UserRepository().delete_user(email,)
    assert success is True, "Delete user failed"
    #verify delete
    user = UserRepository().get_user_by_id(user["user_id"],)
    assert user is None, "User should be None after deletion"
    
def test_delete_receipt():
    receipt_id = receipt["receipt_id"]
    receipt = ReceiptRepository().get_receipt_by_id(receipt_id)
    assert receipt is None, "Receipt should be None after user deletion"
    
    