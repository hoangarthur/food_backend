import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from repositories import UserRepository
import pytest
userDb = {
    "user_id": None,
    "email": "example@gmail.com",
    "password": "examplepassword",
    "new_email": "newexample@gmail.com",
    "new_password": "newexamplepassword"
}

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

def test_create_user_with_existing_email():
    email = userDb['email']
    password = "securepassword"
    with pytest.raises(Exception):
        UserRepository().create_user(email, password)

#get user from database by id
def test_get_user_by_id():
    user_id = userDb['user_id']
    assert user_id is not None, "User ID should not be None"
    users = UserRepository().get_user_by_id(user_id,)
    assert users is not None, "User should not be None"
    assert users["email"] == "example@gmail.com"

#update user email in database by id
def update_user_email_in_db():
    user_id = userDb['user_id']
    success = UserRepository().update_user_email(user_id, userDb['new_email'])
    assert success is True, "Update email failed"
    #verify update
    users = UserRepository().get_user_by_id(user_id,)
    assert users["email"] == userDb['new_email']
     
#Test update user password
def test_update_user_password():
    email = userDb["email"]
    new_password = userDb["new_password"]
    success = UserRepository().update_user_password(email, new_password)
    assert success is True, "Update password failed"
    #verify update
    users = UserRepository().get_user_by_id(userDb["user_id"],)
    assert users["password"] == new_password

#delete user from database by email
def test_delete_user_from_db():
    email = userDb['email']
    success = UserRepository().delete_user(email,)
    assert success is True, "Delete user failed"
    #verify delete
    users = UserRepository().get_user_by_id(userDb["user_id"],)
    assert users is None, "User should be None after deletion"