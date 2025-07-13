from pydantic import EmailStr

from app.dao.user_dao import UserDAO
from app.config import verify_password

async def authentication_user(email: EmailStr, password: str):
    user = await UserDAO.find_one_or_none(email=email)
    if not user or not verify_password(password=password, hashed_password=user.password):
        return None
    return user

