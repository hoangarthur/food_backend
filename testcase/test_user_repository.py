import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from repositories import UserRepository
import pytest
user = {
    "user_id": None,
    "email": "example@gmail.com",
    "password": "examplepassword",
    "new_email": "newexample@gmail.com",
    "new_password": "newexamplepassword"
}

#add new user to database
def test_create_user():
    email = user["email"]
    password = user["password"]
    userID = UserRepository().create_user(email, password)
    user['user_id'] = userID
    assert userID is not None, "Failed to create user"

def test_create_user_with_existing_email():
    email = user["email"]
    password = "securepassword"
    with pytest.raises(Exception):
        UserRepository().create_user(email, password)

#get user from database by id
def test_get_user_by_id():
    user_id = user.get("user_id")
    assert user_id is not None, "User ID should not be None"
    user = UserRepository().get_user_by_id(user_id,)
    assert user is not None, "User should not be None"
    assert user["email"] == "example@gmail.com"

#update user email in database by id
def update_user_email_in_db():
    user_id = user['user_id']
    success = UserRepository().update_user_email(user_id, user['new_email'])
    assert success is True, "Update email failed"
    #verify update
    user = UserRepository().get_user_by_id(user_id,)
    assert user["email"] == user['new_email']
     
#Test update user password
def test_update_user_password():
    email = user["email"]
    new_password = user["new_password"]
    success = UserRepository().update_user_password(email, new_password)
    assert success is True, "Update password failed"
    #verify update
    user = UserRepository().get_user_by_id(user["user_id"],)
    assert user["password"] == new_password

#delete user from database by email
def test_delete_user_from_db():
    email = user['email']
    success = UserRepository().delete_user(email,)
    assert success is True, "Delete user failed"
    #verify delete
    user = UserRepository().get_user_by_id(user["user_id"],)
    assert user is None, "User should be None after deletion"