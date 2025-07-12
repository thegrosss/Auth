from pydantic_settings import BaseSettings

class Settings():
    DB_HOST: str = "localhost"
    DB_PORT: str = "5432"
    DB_NAME: str = "UsersDB"
    DB_USER: str = "thegrosss"
    DB_PASSWORD: str = "VBRZTF3MD3RK"
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