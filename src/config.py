from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    PROJECT_NAME: str = "Shop API"
    # По умолчанию SQLite — запускается без внешних сервисов.
    # Для MySQL: mysql+pymysql://user:password@host:3306/shop_db
    DATABASE_URL: str = "sqlite:///./shop.db"


settings = Settings()
