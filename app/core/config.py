from pydantic_settings import SettingsConfigDict,BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str = "change-me-in-production-use-a-long-random-string"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    PROJECT_NAME: str = "Payment Platform"
    VERSION: str = "0.1.0"
    API_PREFIX: str = "/api"
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")  

settings = Settings()