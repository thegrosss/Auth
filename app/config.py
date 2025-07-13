from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta

class Settings():
    # DB_HOST: str = "localhost"
    # DB_PORT: str = "5432"
    # DB_NAME: str = "UsersDB"
    # DB_USER: str = "thegrosss"
    # DB_PASSWORD: str = "VBRZTF3MD3RK"
    DB_KEY: str = "postgres"
    DB_ALGORITHM: str = "HS256"


settings = Settings()

def get_db_url():
    return "sqlite+aiosqlite:///./database.db"

def get_auth_data():
    return {
        "SECRET_KEY" : settings.DB_KEY,
        "ALGORITHM" : settings.DB_ALGORITHM
        }

crypt = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    password_hash = crypt.hash(password)
    return password_hash

def verify_password(password: str, hashed_password: str) -> bool:
    return crypt.verify(password, hashed_password)

def create_access_token(data: dict) -> str:
    pers_data = data.copy()
    exp_time = datetime.now() + timedelta(days=1)
    pers_data.update({"exp" : exp_time})
    auth_data = get_auth_data()
    token = jwt.encode(pers_data, key=auth_data["SECRET_KEY"], algorithm=auth_data["ALGORITHM"])
    return token