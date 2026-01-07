import json
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from repositories import RecipeRepository, UserRepository
import pytest
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

#add new user to database
def test_create_user():
    email = userDb["email"]
    password = userDb["password"]
    userDb['user_id'] = UserRepository().get_userId_by_email(email,)
    if userDb['user_id'] is not None:
        pytest.skip("User with this email already exists")
    userID = UserRepository().create_user(email, password)
    userDb['user_id'] = userID
    assert userID is not None, "Failed to create user"

def test_create_new_recipe():
    user_id = userDb["user_id"]
    recipe_data["recipe_id"] = RecipeRepository().create_recipe(user_id)
    recipes = RecipeRepository().get_recipe_by_id(recipe_data["recipe_id"],)
    assert recipes is not None, "Failed to create recipe"

def test_update_recipe():
    recipe_id = recipe_data.get("recipe_id")
    recipe_update = recipe_data
    success = RecipeRepository().update_recipe(recipe_id, recipe_update)
    assert success is True, "Update recipe failed"
    updated_recipe = RecipeRepository().get_recipe_by_id(recipe_id,)
    assert updated_recipe['title'] == recipe_data['title'], "Recipe title not updated correctly"
    assert updated_recipe['description'] == recipe_data['description'], "Recipe description not updated correctly"
    #ingredients and instructions are stored as json, must be converted back to list for comparison
    assert json.loads(updated_recipe['ingredients']) == recipe_data['ingredients'], "Recipe ingredients not updated correctly"
    assert json.loads(updated_recipe['instructions']) == recipe_data['instructions'], "Recipe instructions not updated correctly"
    assert updated_recipe['source'] == recipe_data['source'], "Recipe source not updated correctly"
    assert updated_recipe['nutrition'] == recipe_data['nutrition'], "Recipe nutrition not updated correctly"
    assert updated_recipe['totalTime'] == recipe_data['totalTime'], "Recipe totalTime not updated correctly"
    assert updated_recipe['dateSaved'].strftime("%Y-%m-%d") == recipe_data['dateSaved'], "Recipe dateSaved not updated correctly"
    assert updated_recipe['servings'] == recipe_data['servings'], "Recipe servings not updated correctly"

#delete user from database by id
def test_delete_user_from_db():
    email = userDb['email']
    success = UserRepository().delete_user(email,)
    assert success is True, "Delete user failed"
    #verify delete
    user = UserRepository().get_user_by_id(userDb["user_id"],)
    assert user is None, "User should be None after deletion"

def test_delete_recipe():
    recipe_id = recipe_data["recipe_id"]
    recipes = RecipeRepository().get_recipe_by_id(recipe_id,)
    assert recipes is None, "Recipe should be None after user deletion"
    
    