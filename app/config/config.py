from pydantic import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str
    MONGO_DB_URL: str
    MONGO_DB_DATABASE: str
    REDIS_URL: str
    

    class Config:
        case_sensitive = True
        env_file = ".env"


settings = Settings()
