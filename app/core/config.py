class Settings():
    DB_URL: str = "sqlite+aiosqlite:///./database.db"
    DB_KEY: str = "31d6cfe0d16ae931b73c59d7e0c089c0"
    DB_ALGORITHM: str = "HS256"

settings = Settings()

def get_auth_data():
    return {
        "SECRET_KEY" : settings.DB_KEY,
        "ALGORITHM" : settings.DB_ALGORITHM
        }