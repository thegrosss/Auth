from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta

from app.config import get_auth_data

crypt = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    password_hash = crypt.hash(password)
    return password_hash

def verify_password(password: str, hash: str) -> bool:
    return crypt.verify(password, hash)

def create_access_token(data: dict) -> str:
    pers_data = data.copy()
    exp_time = datetime.now() + timedelta(days=1)
    pers_data.update({"exp" : exp_time})
    auth_data = get_auth_data()
    token = jwt.encode(pers_data, key=auth_data["SECRET_KEY"], algorithm=auth_data["ALGORITHM"])
    return token

