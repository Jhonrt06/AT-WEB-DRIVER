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

            page.mouse.move(100, 200)
            page.wait_for_timeout(500)
            page.mouse.wheel(0, 300)

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
            
            logger.info("Clicking on the Electronics option...")
            
            utils.click_by_exact_text(
                    css_selector=SELECTORS_AMAZON["hamburger_option_template"],
                    exact_text="Electrónicos",
            )
            page.wait_for_timeout(1000)
            utils.click_hamburger_item_by_label(
                    label="Televisión y Video",
            )
            page.wait_for_timeout(1000)

            utils.click_text_block_by_label(label='DE 48" A 55"')
            page.wait_for_timeout(1000)

            utils.click_first_product()
            page.wait_for_timeout(1000)

            utils.wait_for_clickable_and_click(SELECTORS_AMAZON["add_to_cart"])
            page.wait_for_timeout(1000)

            utils.close_warranty_popup()
            page.wait_for_timeout(1000)

            # Paso 3: Verificar que se haya añadido al carrito
            if utils.confirm_add_to_cart():
                logger.info("🟢 Flow completed: item added to cart.")
            else:
                logger.warning("🔴 Flow warning: item may NOT have been added.")

            utils.wait_for_clickable_and_click(SELECTORS_AMAZON["nav_cart"])
            page.wait_for_timeout(1000)

            utils.wait_for_clickable_and_click(SELECTORS_AMAZON["buy_now"])
            page.wait_for_timeout(1000)
            logger.info("🟢 Flow completed: item added to cart and proceeding to checkout.")

            input("Press Enter to continue...")  # Pausa para permitir al usuario ver la acción