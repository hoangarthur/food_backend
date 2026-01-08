from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_async_db
from app.repositories import UserRepository

router = APIRouter()
router.prefix = "/users"
router.tags = ["users"]

@router.get("/{email}")
async def get_user_by_email(email: str, db: AsyncSession = Depends(get_async_db)):
    user_repo = UserRepository(db)
    user_id = await user_repo.get_userId_by_email(email)
    if not user_id:
        raise HTTPException(status_code=404, detail="User not found")
    return {"id": user_id}

@router.post("/")
async def create_user(userpackage: dict, db: AsyncSession = Depends(get_async_db)):
    user_repo = UserRepository(db)
    new_user_id = await user_repo.create_user(email=userpackage["email"], password=userpackage["password"])
    return {"id": new_user_id}

@router.put("/{email}/password")
async def update_user_password(email: str, new_password: str, db: AsyncSession = Depends(get_async_db)):
    user_repo = UserRepository(db)
    updated = await user_repo.update_user_password(email=email, new_password=new_password)
    if not updated:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "Password updated successfully"}

@router.delete("/{email}")
async def delete_user(email: str, db: AsyncSession = Depends(get_async_db)):
    user_repo = UserRepository(db)
    deleted = await user_repo.delete_user(email=email)
    if not deleted:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted successfully"}