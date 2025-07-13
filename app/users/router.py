from fastapi import APIRouter, HTTPException, status, Depends, Response
from typing import Annotated

from app.config import get_password_hash, create_access_token
from app.users.schemas import UserModelAdd, UserSchema, UserAuth
from app.dao.user_dao import UserDAO
from app.users.schemas import UserID
from app.users.auth import authentication_user

router = APIRouter(prefix="/auth", tags=["Users"])

@router.get("")
async def get_all_users() -> list[UserSchema]:
    users = await UserDAO.get_all_users()
    return users

@router.post("/register")
async def register(user_data: Annotated[UserModelAdd, Depends()]
)-> UserID:

    user = await UserDAO.find_one_or_none(email=user_data.email)

    if user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Пользователь уже зарегистрирован"
        )

    user_data.password = get_password_hash(user_data.password)
    user_id = await UserDAO.add(user_data)

    return {"message": "Вы успешно зарегистрировались", "id": user_id}

@router.post("/login")
async def login(user_data: Annotated[UserAuth, Depends()], response: Response):
    user_check = await (authentication_user(email=user_data.email, password=user_data.password))

    if user_check is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Неверная почта или пароль")

    access_token = create_access_token({"sub" : str(user_check.id)})
    response.set_cookie(key="users_access_token", value=access_token, httponly=True)
    return {"access_token" : access_token}