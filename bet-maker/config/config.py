from pydantic_settings import BaseSettings, SettingsConfigDict

class RedisSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='./.env', env_file_encoding='utf-8', extra='allow')

    REDIS_URL: str

class PostgresSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='./.env', env_file_encoding='utf-8', extra='allow')

    POSTGRES_PORT: int
    POSTGRES_PASSWORD: str
    POSTGRES_USER: str
    POSTGRES_DB: str
    POSTGRES_HOST: str
    SQLALCHEMY_DATABASE_URL: str


class JWTsettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='./.env', env_file_encoding='utf-8', extra='allow')

    JWT_PUBLIC_KEY: str
    JWT_PRIVATE_KEY: str
    REFRESH_TOKEN_EXPIRES_IN: int
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    JWT_ALGORITHM: str


class Settings(BaseSettings):
    model_config = SettingsConfigDict(extra='allow')
    db: PostgresSettings = PostgresSettings()
    jwt: JWTsettings = JWTsettings()
    redis: RedisSettings = RedisSettings()


settings = Settings(_env_file='./.env', _env_file_encoding='utf-8')
