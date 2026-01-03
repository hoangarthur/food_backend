# repositories/receipt_repository.py
from repositories.item_repository import ItemRepository
from core.database import get_db_connection

class RecipeRepository:
    """Repository for recipe-related database operations"""
    def get_recipe_by_id(self, recipe_id):
        """Fetch a recipe by its ID"""
        with get_db_connection() as conn:
            cursor = conn.cursor(dictionary=True)
            query = "SELECT * FROM recipes WHERE id = %s"
            cursor.execute(query, (recipe_id,))
            recipe = cursor.fetchone()
            return recipe
    
    def get_recipes_by_user(self, user_id):
        """Fetch all recipes for a specific user"""
        with get_db_connection() as conn:
            cursor = conn.cursor(dictionary=True)
            query = "SELECT * FROM recipes WHERE user_id = %s"
            cursor.execute(query, (user_id,))
            recipes = cursor.fetchall()
            return recipes

    def check_recipe_exists(self, recipe_id):
        """Check if a recipe exists by ID"""
        with get_db_connection() as conn:
            cursor = conn.cursor(dictionary=True)
            query = "SELECT COUNT(*) as count FROM recipes WHERE id = %s"
            cursor.execute(query, (recipe_id,))
            result = cursor.fetchone()
            return result['count'] > 0

    # added method
    def create_recipe(self, recipe_id, user_id, item):
        """Create a new recipe and associated items"""
        with get_db_connection() as conn:
            cursor = conn.cursor()
            query = "INSERT INTO recipes (id, user_id) VALUES (%s, %s)"
            cursor.execute(query, (recipe_id, user_id,))
            conn.commit()
        item_repo = ItemRepository()
        for it in item:
            item_repo.create_item(it['name'], it['price'], it['quantity'], it['date'], it['store'], it['category'], recipe_id)
         #Todo: return http response indicating creation

    def delete_recipe_by_id(self, recipe_id):
        """Delete a recipe by ID"""
        with get_db_connection() as conn:
            cursor = conn.cursor()
            query = "DELETE FROM recipes WHERE id = %s"
            cursor.execute(query, (recipe_id,))
            conn.commit()
            return cursor.rowcount > 0