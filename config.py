'''configaration settings for the application'''

from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_hostname: str
    database_port: str
    database_password: str
    database_name: str
    database_username: str
    secret_key: str

    class Config:
        env_file = ".env"

settings = Settings()