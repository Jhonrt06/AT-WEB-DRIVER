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
        with BaseBot(headless=False) as bot:
            page = bot.page
            utils = PlaywrightUtils(page)

            utils.open_page(self.settings.amazon_url)
            page.wait_for_timeout(1000)
            if utils.verify_element(
                "form[action='/errors/validateCaptcha']", timeout=2000
            ):
                logger.warning(
                    "⚠️ CAPTCHA detected. Manual intervention required."
                )
                input("Solve CAPTCHA and press ENTER to continue...")

            self.login_amazon(utils)
            # self.search_product(utils, product_name)

    def login_amazon(self, utils):
        logger.info("Logging in...")
        utils.wait_and_click(SELECTORS_AMAZON["login_button_home"])
        utils.login(self.email, self.password, SELECTORS_AMAZON)
        logger.info("Login completed.")
