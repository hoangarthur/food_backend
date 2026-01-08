import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import json
import pytest
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from repositories import ReceiptRepository, UserRepository, ItemRepository, RecipeRepository

# Synchronous engine + session
engine = create_engine("sqlite:///:memory:", echo=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def session():
    """Create a new database session for a test."""
    session = SessionLocal()
    
    # Drop tables first to ensure clean state + correct cascade
    session.execute(text("DROP TABLE IF EXISTS receipts"))
    session.execute(text("DROP TABLE IF EXISTS recipes"))
    session.execute(text("DROP TABLE IF EXISTS users"))
    
    # Create tables in correct order
    session.execute(text("""
        CREATE TABLE users (
            userId INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """))
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
    # Assuming you have receipts table too - add it if needed
    session.execute(text("""
        CREATE TABLE IF NOT EXISTS receipts (
            receiptId INTEGER PRIMARY KEY AUTOINCREMENT,
            userId INTEGER NOT NULL,
            source TEXT,
            status TEXT,
            date DATE,
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

recipe_data = {
    "recipe_id": None,
    "user_id": None,
    "title": "Sample Recipe Title",
    "description": "Sample Recipe Description",
    "ingredients": ["Sample Item 1", "Sample Item 3"],
    "instructions": ["instruction1", "instruction2"],
    "source": "Sample Source",
    "nutrition": 100,
    "totalTime": 30,
    "dateSaved": "2024-01-01",
    "servings": 4
}

itemsList = [
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
    "store": "Sample Store",
    "category": "Sample Category"
    }
]

def test_recipe(session):
    global recipe_data, userDb, itemsList
    User_Repo = UserRepository(session)
    Recipe_Repo = RecipeRepository(session)
    email = userDb["email"]
    password = userDb["password"]
    userDb['user_id'] = User_Repo.get_userId_by_email(email,)
    if userDb['user_id'] is not None:
        pytest.skip("User with this email already exists")
    userID = User_Repo.create_user(email, password)
    session.commit()
    userDb['user_id'] = userID
    assert userID is not None, "Failed to create user"
    #test create recipe
    recipe_data["recipe_id"] = Recipe_Repo.create_recipe(userDb["user_id"],)
    session.commit()
    recipes = Recipe_Repo.get_recipe_by_id(recipe_data["recipe_id"])
    assert recipes is not None, "Failed to create recipe"
    #test update recipe
    recipe_id = recipe_data.get("recipe_id")
    recipe_update = recipe_data
    success = Recipe_Repo.update_recipe(recipe_id, recipe_update)
    session.commit()
    assert success is True, "Update recipe failed"
    updated_recipe = Recipe_Repo.get_recipe_by_id(recipe_id,)
    assert updated_recipe is not None, "Could not find updated recipe"
    assert updated_recipe['title'] == recipe_data['title'], "Recipe title not updated correctly"
    assert updated_recipe['description'] == recipe_data['description'], "Recipe description not updated correctly"
    # ingredients and instructions are stored as json
    assert json.loads(updated_recipe['ingredients']) == recipe_data['ingredients'], "Recipe ingredients not updated correctly"
    assert json.loads(updated_recipe['instructions']) == recipe_data['instructions'], "Recipe instructions not updated correctly"
    assert updated_recipe['source'] == recipe_data['source'], "Recipe source not updated correctly"
    assert updated_recipe['nutrition'] == recipe_data['nutrition'], "Recipe nutrition not updated correctly"
    assert updated_recipe['totalTime'] == recipe_data['totalTime'], "Recipe totalTime not updated correctly"
    assert updated_recipe['servings'] == recipe_data['servings'], "Recipe servings not updated correctly"
    #test delete user and cascade delete recipe
    email = userDb['email']
    success = User_Repo.delete_user(email,)
    session.commit()
    assert success is True, "Delete user failed"
    success = Recipe_Repo.delete_recipe_by_id(recipe_id,)
    session.commit()
    #verify delete
    user = User_Repo.get_user_by_id(userDb["user_id"],)
    assert user is None, "User should be None after deletion"
    #verify recipe delete cascade
    recipe_id = recipe_data["recipe_id"]
    recipes = Recipe_Repo.get_recipe_by_id(recipe_id,)
    assert recipes is None, "Recipe should be None after user deletion"