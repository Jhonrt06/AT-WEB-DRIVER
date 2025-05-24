from automation.base_bot import BaseBot
from automation.playwright_utils import PlaywrightUtils
from config.settings import Settings
from automation.playwright_constants import SELECTORS_AMAZON
from config.logs.logger_config import logger
from playwright.sync_api import *


class BuyBot:
    """
    Test case: automation of the purchase flow.
    Contains methods to open Amazon and perform login.
    """

    def __init__(self, email, password):
        self.email = email
        self.password = password
        self.settings = Settings()

    def run_purchase_flow(self, product_name=None):
        logger.info("Starting the purchase flow...")

        with BaseBot(headless=False) as bot:
            page = bot.page
            utils = PlaywrightUtils(page)
            page.wait_for_timeout(1000)  # 1 second pause

            logger.info("Opening Amazon...")
            utils.open_page(self.settings.amazon_url)
            page.wait_for_timeout(1000)

            logger.info("Clicking on the login button...")
            utils.wait_for_clickable_and_click(SELECTORS_AMAZON["login_button_home"])
            page.wait_for_timeout(1000)

            logger.info("Login")
            utils.login(
                    email=self.email,
                    password=self.password,
                    selectors=SELECTORS_AMAZON,
            )
            page.wait_for_timeout(1000)

            logger.info("Verifying login...")
            # Wait for the page to load and check if the login was successful
            utils.validate_login(
                    selector=SELECTORS_AMAZON["login_button_home"],
            )
            page.wait_for_timeout(1000)

            logger.info("Verify and Click on the hamburger menu...")
            utils.wait_for_clickable_and_click(SELECTORS_AMAZON["hamburger_menu"])
            page.wait_for_timeout(1000)
            # Wait for the user to verify the login manually
        input("✅ Press ENTER after verifying login manually...")



