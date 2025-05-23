from dotenv import load_dotenv
import os

# Load environment variables from the .env file
load_dotenv()


class Settings:
    """
    Class that loads and manages the project's environment variables.

    This class is responsible for reading the variables defined in the `.env` file
    using the `python-dotenv` library and provides safe access to them throughout the code.

    Attributes:
    -----------
    amazon_url : str
        Base URL of the Amazon site to be used in the automation.

    headless : bool
        Defines whether the browser should run in headless (invisible) mode
        or headed (visible) mode. Expected values are 'true' or 'false' as strings.
    """

    def __init__(self):
        self.amazon_url = os.getenv("AMAZON_URL")
        self.headless = os.getenv("HEADLESS", "true").lower() == "true"
