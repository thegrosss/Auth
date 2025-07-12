from fastapi import APIRouter, HTTPException, status, Depends
from typing import Annotated

from app.users.schemas import UserModelAdd, UserModel
from app.users.dao import BaseDAO
from app.users.schemas import UserID

router = APIRouter(prefix="/users", tags=["Users"])

@router.get("")
async def get_all_users() -> list[UserModel]:
    users = await BaseDAO.get_all_users()
    return users

@router.post("/register")
async def register(user_data: Annotated[UserModelAdd, Depends()]
)-> UserID:

    user = await BaseDAO.find_one_or_none(email=user_data.email)

    if user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Пользователь уже зарегистрирован"
        )

    user_id = await BaseDAO.add(user_data)

    return {"message": "Вы успешно зарегистрировались",
            "id": user_id}