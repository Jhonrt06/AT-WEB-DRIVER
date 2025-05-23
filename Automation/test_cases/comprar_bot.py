from automation.base_bot import BaseBot
from automation.playwright_utils import PlaywrightUtils
from config.settings import Settings
from automation.playwright_constants import SELECTORS_AMAZON
from config.logs.logger_config import logger

class ComprarBot:
    """
    Test case: automation of the purchase flow.
    Contains methods to open Amazon and perform login.
    """

    def __init__(self, email, password):
        self.email = email
        self.password = password
        self.settings = Settings()
        # self.headless = self.settings.headless

    def open_amazon(self):
        logger.info("Opening Amazon...")
        with BaseBot(headless=False) as bot:
            page = bot.page
            page.goto(self.settings.amazon_url)
            print("✅ Amazon opened successfully.")
            input("Press ENTER to close the browser...")

    def login_amazon(self):
        logger.info("Starting login on Amazon...")
        with BaseBot(headless=self.settings.headless) as bot:
            page = bot.page
            page.goto("https://www.amazon.com.mx/ap/signin")

            utils = PlaywrightUtils(page)
            utils.login(
                self.email, self.password, SELECTORS_AMAZON["login_button_home"]
            )

            print("✅ Login completed.")
            input("Press ENTER to close the browser...")
