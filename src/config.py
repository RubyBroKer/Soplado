from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    
    DATABASE_URL : str
    JWT_SECRET_KEY : str
    JWT_ALGORITHM : str
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    OPENCAGE_API_KEY: str
    KAFKA_BOOTSTRAP_SERVERS: str = "localhost:9092"
    KAFKA_TOPIC : str = "bookings"

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )

Config = Settings()