from fastapi import Request, HTTPException, status, Depends
from jose import jwt, JWTError
from datetime import datetime

from app.core.config import get_auth_data
from app.dao.user_dao import UserDAO
from app.users.models import User


def get_token(request: Request):
    token = request.cookies.get("users_access_token")
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token not found")
    return token

async def get_current_user(token: str = Depends(get_token)):
    try:
        auth_data = get_auth_data()
        token_decode = jwt.decode(token, key=auth_data['SECRET_KEY'], algorithms=[auth_data['ALGORITHM']])
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Токен не валидный")

    exp = token_decode.get('exp')
    if not exp or datetime.fromtimestamp(int(exp)) < datetime.now():
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Время действия токена истекло")

    user_id = token_decode.get('sub')
    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Пользователь с таким ID не найден")

    user = await UserDAO.find_one_or_none(id=user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Пользователь не найден")

    return user

async def get_current_admin_user(user_data: User = Depends(get_current_user)):
    if user_data.is_admin:
        return user_data
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Недостаточно прав")