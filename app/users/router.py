from fastapi import APIRouter, HTTPException, status, Depends, Response
from typing import Annotated

from app.core.security import get_password_hash, create_access_token
from app.users.models import User
from app.users.schemas import UserModelAdd, UserSchema, UserAuth, UserID, UserRoles
from app.dao.user_dao import UserDAO
from app.users.auth import authentication_user
from app.core.dependencies import get_current_user, get_current_admin_user

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/auth/register")
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

    return UserID(id=user_id)

@router.post("/auth/login")
async def login(user_data: Annotated[UserAuth, Depends()], response: Response):
    user_check = await (authentication_user(email=user_data.email, password=user_data.password))

    if user_check is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Неверная почта или пароль")

    access_token = create_access_token({"sub" : str(user_check.id)})
    response.set_cookie(key="users_access_token", value=access_token, httponly=True)
    return {"access_token" : access_token}

@router.post("/auth/logout")
async def logout(response: Response):
    response.delete_cookie(key="users_access_token")
    return {"message" : "Пользователь успешно вышел из системы"}

@router.get("/me")
async def get_me(user_data: User = Depends(get_current_user)):
    return user_data

@router.get("")
async def get_all_users(admin: User = Depends(get_current_admin_user)) -> list[UserSchema]:
    users = await UserDAO.get_all_users()
    return users

@router.post("/roles")
async def change_user_role(user_id: int,
                           role: UserRoles,
                           value: bool,
                           admin: User = Depends(get_current_admin_user)):
    user = await UserDAO.find_one_or_none(id=user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Пользователь не найден")
    else:
        await UserDAO.change_role(user_id, role.value, value)
        return {"message" : f"Изменена роль '{role.value}' пользователя {user.id}"}
