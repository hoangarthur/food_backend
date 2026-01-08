# repositories/user_repository.py
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text

class UserRepository:
    """Repository for user-related database operations"""
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def get_user_by_id(self, user_id: int) -> dict:
        """Fetch a user by their ID"""    
        result = await self.session.execute(
            text("SELECT * FROM users WHERE userId = :user_id"),
            {"user_id": user_id}
        )
        return result.mappings().first()
            
    async def get_userId_by_email(self, email):
        """Fetch a user's ID by their email"""
        result = await self.session.execute(
            text("SELECT userId FROM users WHERE email = :email"),
            {"email": email}
        )
        return result.scalar()

        
    async def check_user_exists(self, email: str) -> bool:
        """Check if a user exists by email"""
        result = await self.session.execute(
            text("SELECT COUNT(*) as count FROM users WHERE email = :email"),
            {"email": email}
        )
        return result.scalar() > 0
    
    async def create_user(self, email: str, password: str) -> int:
        """Create a new user"""
        if await self.check_user_exists(email):
            raise ValueError("User with this email already exists")

        result = await self.session.execute(
            text("INSERT INTO users (email, password) VALUES (:email, :password)"),
            {"email": email, "password": password}
        )
        await self.session.commit()
        return result.lastrowid
        
    async def update_user_password(self, email:str, new_password:str)-> bool:
        """Update a user's password by email""" 
        result = await self.session.execute(
            text("UPDATE users SET password = :new_password WHERE email = :email"),
            {"new_password": new_password, "email": email}
        )
        await self.session.commit()
        return result.rowcount > 0
    
    async def delete_user(self, email) -> bool:
        """delete a user by email"""
        result = await self.session.execute(
            text("DELETE FROM users WHERE email = :email"),
            {"email": email}
        )        
        await self.session.commit()
        return result.rowcount > 0
    