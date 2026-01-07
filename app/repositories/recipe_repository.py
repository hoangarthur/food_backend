# repositories/recipe_repository.py
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
import json
from typing import Dict, Any, Optional

class RecipeRepository:
    """Repository for recipe-related database operations"""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_recipe_by_id(self, recipe_id: int) -> Optional[Dict[str, Any]]:
        """Fetch a recipe by its ID"""
        result = await self.session.execute(
            text("SELECT * FROM recipes WHERE recipeId = :recipe_id"),
            {"recipe_id": recipe_id}
        )
        return result.mappings().first()  # return dict or None

    async def get_recipes_by_user(self, user_id: int) -> list[Dict[str, Any]]:
        """Fetch all recipes for a specific user"""
        result = await self.session.execute(
            text("SELECT * FROM recipes WHERE userId = :user_id"),
            {"user_id": user_id}
        )
        return result.mappings().all()  # return list of dicts

    async def check_recipe_exists(self, recipe_id: int) -> bool:
        """Check if a recipe exists by ID"""
        result = await self.session.execute(
            text("SELECT COUNT(*) as count FROM recipes WHERE recipeId = :recipe_id"),
            {"recipe_id": recipe_id}
        )
        return result.scalar() > 0

    async def create_recipe(self, user_id: int) -> int:
        """Create a new recipe and return new recipe_id"""
        result = await self.session.execute(
            text("INSERT INTO recipes (userId) VALUES (:user_id)"),
            {"user_id": user_id}
        )
        await self.session.commit()
        return result.lastrowid

    async def update_recipe(self, recipe_id: int, updated_data: Dict[str, Any]) -> bool:
        """Update a recipe and return True if successful"""
        # Check existence first
        if not await self.check_recipe_exists(recipe_id):
            raise ValueError(f"Recipe with ID {recipe_id} does not exist")

        # Convert lists to JSON strings
        ingredients = json.dumps(updated_data.get("ingredients", []))
        instructions = json.dumps(updated_data.get("instructions", []))

        result = await self.session.execute(
            text("""
                UPDATE recipes
                SET source = :source,
                    title = :title,
                    description = :description,
                    ingredients = :ingredients,
                    instructions = :instructions,
                    nutrition = :nutrition,
                    totalTime = :totalTime,
                    dateSaved = :dateSaved,
                    servings = :servings
                WHERE recipeId = :recipe_id
            """),
            {
                "source": updated_data.get("source"),
                "title": updated_data.get("title"),
                "description": updated_data.get("description"),
                "ingredients": ingredients,
                "instructions": instructions,
                "nutrition": updated_data.get("nutrition"),
                "totalTime": updated_data.get("totalTime"),
                "dateSaved": updated_data.get("dateSaved"),
                "servings": updated_data.get("servings"),
                "recipe_id": recipe_id
            }
        )
        await self.session.commit()
        return result.rowcount > 0

    async def delete_recipe_by_id(self, recipe_id: int) -> bool:
        """Delete a recipe by ID and return True if successful"""
        result = await self.session.execute(
            text("DELETE FROM recipes WHERE recipeId = :recipe_id"),
            {"recipe_id": recipe_id}
        )
        await self.session.commit()
        return result.rowcount > 0