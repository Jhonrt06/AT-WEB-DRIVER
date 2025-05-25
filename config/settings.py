from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    amazon_url: str
    headless: bool = True
    api_host: str = "127.0.0.1"
    api_port: int = 8000

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"
