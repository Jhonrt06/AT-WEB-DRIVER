from automation.base_bot import BaseBot
from automation.playwright_utils import PlaywrightUtils
from automation.playwright_constants import SELECTORS_AMAZON
from config.settings import Settings
from config.logs.logger_config import logger
from playwright.sync_api import Page


class BuyBot:
    """
    Automates the Amazon purchase flow: login, navigation, and product purchase.
    """

    def __init__(self, email: str, password: str, headless: bool, amazon_url: str):
        """
        Initializes the BuyBot with user credentials and settings.

        Args:
            email (str): User's email address.
            password (str): User's password.
        """
        self.email = email
        self.password = password
        self.headless = headless
        self.amazon_url = amazon_url

    def run_purchase_flow(self) -> None:
        """
        Executes the full purchase flow on Amazon using Playwright.
        """
        logger.info("🚀 Starting the purchase flow...")

        with BaseBot(headless=self.headless) as bot:
            page: Page = bot.page
            utils = PlaywrightUtils(page)

            logger.info("🌐 Opening Amazon homepage...")
            utils.open_page(self.amazon_url)

            logger.info("🔐 Navigating to login...")
            utils.wait_for_clickable_and_click(
                SELECTORS_AMAZON["login_button_home"]
            )
            utils.login(
                email=self.email,
                password=self.password,
                selectors=SELECTORS_AMAZON,
            )

            logger.info("🔍 Verifying successful login...")
            login_success = utils.validate_login(
                SELECTORS_AMAZON["login_button_home"]
            )
            if not login_success:
                logger.error("❌ Login validation failed. Aborting flow.")
                return

            logger.info("📂 Opening hamburger menu...")
            utils.wait_for_clickable_and_click(
                SELECTORS_AMAZON["hamburger_menu"]
            )

            logger.info("📁 Selecting 'Electrónicos' category...")
            utils.click_by_exact_text(
                css_selector=SELECTORS_AMAZON["hamburger_option_template"],
                exact_text="Electrónicos",
            )

            logger.info("📺 Selecting 'Televisión y Video' subcategory...")
            utils.click_hamburger_item_by_label("Televisión y Video")

            logger.info("📏 Filtering by size 'DE 48\" A 55\"'...")
            utils.click_text_block_by_label('DE 48" A 55"')

            logger.info("🛍️ Clicking the first visible product...")
            utils.click_first_product()

            logger.info("➕ Adding product to cart...")
            utils.wait_for_clickable_and_click(SELECTORS_AMAZON["add_to_cart"])

            logger.info("🔧 Checking for warranty popup...")
            utils.close_warranty_popup()

            logger.info("🧾 Confirming product is in the cart...")
            if utils.confirm_add_to_cart():
                logger.info("✅ Item successfully added to cart.")
            else:
                logger.warning("⚠️ Item may not have been added to the cart.")

            logger.info("🛒 Navigating to cart...")
            utils.wait_for_clickable_and_click(SELECTORS_AMAZON["nav_cart"])

            logger.info("💳 Proceeding to checkout...")
            utils.wait_for_clickable_and_click(SELECTORS_AMAZON["buy_now"])

            logger.info("🏁 Purchase flow completed successfully.")
