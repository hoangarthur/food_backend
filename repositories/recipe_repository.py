# repositories/receipt_repository.py
from flask import json
from repositories.item_repository import ItemRepository
from core.database import get_db_connection

class RecipeRepository:
    """Repository for recipe-related database operations"""
    def get_recipe_by_id(self, recipe_id):
        """Fetch a recipe by its ID"""
        with get_db_connection() as conn:
            cursor = conn.cursor(dictionary=True)
            query = "SELECT * FROM recipes WHERE recipeId = %s"
            cursor.execute(query, (recipe_id,))
            recipe = cursor.fetchone()
            return recipe
    
    def get_recipes_by_user(self, user_id):
        """Fetch all recipes for a specific user"""
        with get_db_connection() as conn:
            cursor = conn.cursor(dictionary=True)
            query = "SELECT * FROM recipes WHERE userId = %s"
            cursor.execute(query, (user_id,))
            recipes = cursor.fetchall()
            return recipes

    def check_recipe_exists(self, recipe_id):
        """Check if a recipe exists by ID"""
        with get_db_connection() as conn:
            cursor = conn.cursor(dictionary=True)
            query = "SELECT COUNT(*) as count FROM recipes WHERE recipeId = %s"
            cursor.execute(query, (recipe_id,))
            result = cursor.fetchone()
            return result['count'] > 0

    # added method  
    def create_recipe(self, user_id):
        """Create a new recipe and associated items"""
        with get_db_connection() as conn:
            cursor = conn.cursor()
            query = "INSERT INTO recipes (userId) VALUES (%s)"
            cursor.execute(query, (user_id,))
            conn.commit()
            return cursor.lastrowid


    def update_recipe(self, recipe_id, updated_data):
        """Update a recipe"""
        self.check_recipe_exists(recipe_id)
        with get_db_connection() as conn:
            cursor = conn.cursor()
            #ingredients and instructions are stored as json, must be converted to json string
            query = """
                UPDATE recipes
                SET source = %s, title = %s, 
                description = %s, ingredients = %s, 
                instructions = %s, nutrition = %s, 
                totalTime = %s, dateSaved = %s, servings = %s
                WHERE recipeId = %s
            """
            ingredients = json.dumps(updated_data.get("ingredients"))
            instructions = json.dumps(updated_data.get("instructions"))
            cursor.execute(query, (
                updated_data.get('source'),
                updated_data.get('title'),
                updated_data.get('description'),
                ingredients,
                instructions,
                updated_data.get('nutrition'),
                updated_data.get('totalTime'),
                updated_data.get('dateSaved'),
                updated_data.get('servings'),
                recipe_id
            ))
            conn.commit()
            return cursor.rowcount > 0

    def delete_recipe_by_id(self, recipe_id):
        """Delete a recipe by ID"""
        with get_db_connection() as conn:
            cursor = conn.cursor()
            query = "DELETE FROM recipes WHERE recipeId = %s"
            cursor.execute(query, (recipe_id,))
            conn.commit()
            return cursor.rowcount > 0