from pydantic_settings import SettingsConfigDict,BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str
    PROJECT_NAME: str = "Payment Platform"
    VERSION: str = "0.1.0"
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")  

settings = Settings()