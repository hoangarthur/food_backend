import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

from repositories.user_repository import UserRepository

# Synchronous engine + session
engine = create_engine("sqlite:///:memory:", echo=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def session():
    """Create a new database session for a test."""
    session = SessionLocal()
    
    session.execute(text("""
        CREATE TABLE IF NOT EXISTS users (
            userId INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """))
    session.commit()
    
    yield session
    session.close()


userDb = {
    "user_id": None,
    "email": "testuser@example.com",
    "password": "testpass123",
    "new_password": "newpass456"
}


def test_create_user(session):
    repo = UserRepository(session)
    email = userDb["email"]
    password = userDb["password"]
    
    if repo.check_user_exists(email):
        repo.delete_user(email)
        session.commit()

    userDb['user_id'] = repo.get_userId_by_email(email)
    if userDb['user_id'] is not None:
        pytest.skip("User with this email already exists")

    userID = repo.create_user(email, password)
    session.commit() 
    userDb['user_id'] = userID

    assert userID is not None, "Failed to create user"
    assert isinstance(userID, int)


def test_create_user_with_existing_email(session):
    repo = UserRepository(session)
    email = userDb["email"]

    if not repo.check_user_exists(email):
        repo.create_user(email, userDb["password"])
        session.commit()

    with pytest.raises(ValueError, match="User with this email already exists"):
        repo.create_user(email, "anotherpass")


def test_get_user_by_id(session):
    repo = UserRepository(session)

    if userDb['user_id'] is None:
        userDb['user_id'] = repo.create_user(userDb["email"], userDb["password"])
        session.commit()

    user = repo.get_user_by_id(userDb['user_id'])
    assert user is not None, "User should be found"
    assert user["email"] == userDb["email"]


def test_update_user_password(session):
    repo = UserRepository(session)

    if userDb['user_id'] is None:
        userDb['user_id'] = repo.create_user(userDb["email"], userDb["password"])
        session.commit()

    success = repo.update_user_password(userDb["email"], userDb["new_password"])
    assert success is True, "Update password failed"

    user = repo.get_user_by_id(userDb['user_id'])
    assert user is not None
 


def test_delete_user_from_db(session):
    repo = UserRepository(session)

    if userDb['user_id'] is None:
        userDb['user_id'] = repo.create_user(userDb["email"], userDb["password"])
        session.commit()

    success = repo.delete_user(userDb["email"])
    assert success is True, "Delete should succeed"

    assert repo.check_user_exists(userDb["email"]) is False
    user = repo.get_user_by_id(userDb['user_id'])
    assert user is None, "User should be gone after deletion"

