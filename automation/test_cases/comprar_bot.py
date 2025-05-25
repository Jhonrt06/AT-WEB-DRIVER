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

            logger.info("Opening Amazon...")
            utils.open_page(self.settings.amazon_url)

            logger.info("Clicking on the login button...")
            utils.wait_for_clickable_and_click(SELECTORS_AMAZON["login_button_home"])

            logger.info("Login")
            utils.login(
                    email=self.email,
                    password=self.password,
                    selectors=SELECTORS_AMAZON,
            )

            logger.info("Verifying login...")
            # Wait for the page to load and check if the login was successful
            utils.validate_login(
                    selector=SELECTORS_AMAZON["login_button_home"],
            )

            logger.info("Verify and Click on the hamburger menu...")
            utils.wait_for_clickable_and_click(SELECTORS_AMAZON["hamburger_menu"])
            logger.info("Clicking on the Electronics option...")
            
            utils.click_by_exact_text(
                    css_selector=SELECTORS_AMAZON["hamburger_option_template"],
                    exact_text="Electrónicos",
            )

            utils.click_hamburger_item_by_label(
                    label="Televisión y Video",
            )

            utils.click_text_block_by_label(label='DE 48" A 55"')


            utils.click_first_product()

            utils.wait_for_clickable_and_click(SELECTORS_AMAZON["add_to_cart"])

            utils.close_warranty_popup()

            # Paso 3: Verificar que se haya añadido al carrito
            if utils.confirm_add_to_cart():
                logger.info("🟢 Flow completed: item added to cart.")
            else:
                logger.warning("🔴 Flow warning: item may NOT have been added.")

            utils.wait_for_clickable_and_click(SELECTORS_AMAZON["nav_cart"])

            utils.wait_for_clickable_and_click(SELECTORS_AMAZON["buy_now"])

            logger.info("🟢 Flow completed: item added to cart and proceeding to checkout.")