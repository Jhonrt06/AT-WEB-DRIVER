from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """
    Application configuration class using Pydantic BaseSettings.

    This class automatically loads environment variables from a `.env` file 
    and provides strongly-typed access to configuration parameters such as:
    - Amazon target URL
    - Headless browser mode
    - API host and port for the FastAPI service

    Attributes:
        amazon_url (str): The base URL for Amazon automation (e.g., https://www.amazon.com.mx).
        headless (bool): Whether to run the browser in headless mode (default: True).
        api_host (str): The host address for the FastAPI server (default: 127.0.0.1).
        api_port (int): The port number for the FastAPI server (default: 8000).
    """

    amazon_url: str
    headless: bool = True
    api_host: str = "127.0.0.1"
    api_port: int = 8000

    class Config:
        """
        Configuration for the BaseSettings class.

        - env_file: Specifies the file to read environment variables from.
        - env_file_encoding: Defines the encoding used for the env file.
        - extra: Controls behavior for unknown environment variables (ignored in this case).
        """
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"
