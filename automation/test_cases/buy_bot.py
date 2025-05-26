from automation.base_bot import BaseBot
from automation.playwright_utils import PlaywrightUtils
from automation.playwright_constants import SELECTORS_AMAZON
from config.settings import Settings
from config.logs.logger_config import logger
from playwright.sync_api import Page


class BuyBot:
    """
    Automates the Amazon purchase flow using Playwright.

    This bot performs a full automated sequence that includes:
    - Opening the Amazon homepage
    - Logging in with user credentials
    - Navigating through categories
    - Filtering and selecting a product
    - Adding the product to the cart
    - Proceeding to checkout

    Attributes:
        email (str): Amazon account email.
        password (str): Amazon account password.
        headless (bool): Whether to run the browser in headless mode.
        url (str): URL to open (e.g., Amazon homepage).
    """

    def __init__(self, email: str, password: str, headless=True, url=None):
        """
        Initializes the BuyBot with the provided user credentials and settings.

        Args:
            email (str): User's Amazon email address.
            password (str): User's Amazon password.
            headless (bool, optional): Run browser headlessly. Defaults to True.
            url (str, optional): URL to navigate to. Usually Amazon homepage.
        """
        self.email = email
        self.password = password
        self.headless = headless
        self.url = url

    def run_purchase_flow(self) -> None:
        """
        Executes the full automated purchase flow on Amazon.
        """
        logger.info("Starting the purchase flow...")

        # Launch the browser with context using BaseBot
        with BaseBot(headless=self.headless) as bot:
            page: Page = bot.page
            utils = PlaywrightUtils(page)

            # Open the Amazon homepage
            logger.info("Opening Amazon homepage...")
            utils.open_page(self.url)

            # Navigate to the login page and perform login
            logger.info("Navigating to login...")
            utils.wait_for_clickable_and_click(SELECTORS_AMAZON["login_button_home"])
            utils.login(
                email=self.email,
                password=self.password,
                selectors=SELECTORS_AMAZON,
            )

            # Validate if login was successful
            logger.info("Verifying successful login...")
            login_success = utils.validate_login(SELECTORS_AMAZON["login_button_home"])
            if not login_success:
                logger.error("Login validation failed. Aborting flow.")
                return

            # Open the hamburger menu (side menu)
            logger.info("Opening hamburger menu...")
            utils.wait_for_clickable_and_click(SELECTORS_AMAZON["hamburger_menu"])

            # Navigate through categories to reach TVs
            logger.info("Selecting 'Electrónicos' category...")
            utils.click_by_exact_text(
                css_selector=SELECTORS_AMAZON["hamburger_option_template"],
                exact_text="Electrónicos",
            )

            logger.info("Selecting 'Televisión y Video' subcategory...")
            utils.click_hamburger_item_by_label("Televisión y Video")

            # Filter by TV size
            logger.info("Filtering by size 'DE 48\" A 55\"'...")
            utils.click_text_block_by_label('DE 48" A 55"')

            # Click on the first product listed
            logger.info("Clicking the first visible product...")
            utils.click_first_product()

            # Add the product to the shopping cart
            logger.info("Adding product to cart...")
            utils.wait_for_clickable_and_click(SELECTORS_AMAZON["add_to_cart"])

            # Close optional warranty popup if it appears
            logger.info("Checking for warranty popup...")
            utils.close_warranty_popup()

            # Confirm product was added to the cart
            logger.info("Confirming product is in the cart...")
            if utils.confirm_add_to_cart():
                logger.info("Item successfully added to cart.")
            else:
                logger.warning("Item may not have been added to the cart.")

            # Go to the cart page
            logger.info("Navigating to cart...")
            utils.wait_for_clickable_and_click(SELECTORS_AMAZON["nav_cart"])

            # Proceed to buy
            logger.info("Proceeding to checkout...")
            utils.wait_for_clickable_and_click(SELECTORS_AMAZON["buy_now"])

            logger.info("Purchase flow completed successfully.")
