from playwright.sync_api import TimeoutError
from config.logs.logger_config import logger
from automation.playwright_constants import SELECTORS_AMAZON
import unicodedata
class PlaywrightUtils:
    """
    PlaywrightUtils class
    Contains reusable methods for interacting with web pages using Playwright.

    Typical usage:
        utils = PlaywrightUtils(page)
        utils.fill_input("#field", "text")
        utils.wait_and_click("#button")
    """

    def __init__(self, page):
        """
        Initializes the utility with a Playwright page instance.

        Parameters:
        - page: Page object created by Playwright (bot.page)
        """
        self.page = page

    def wait_for_clickable_and_click(self, selector: str, timeout=10000):
        """
        Waits for an element to be clickable and clicks it. Logs the outcome.

        Args:
            selector (str): CSS selector of the element.
            timeout (int): Max wait time (in ms).
        """
        logger.info(f"Waiting for element {selector!r} to be clickable...")
        body_text = self.get_visible_text(selector, timeout)


        try:
            self.page.wait_for_selector(selector, timeout=timeout, state="visible")
            locator = self.page.locator(selector)

            if locator.is_enabled():
                locator.click()
                logger.info(f'✅ "{body_text}" has been pressed.')
            else:
                logger.warning(f'⚠️ "{body_text}" is visible but not enabled (not clickable).')
        except Exception as e:
            logger.error(f'❌ Failed to click "{body_text or selector}": {e}')

    def login(self, email: str, password: str, selectors: dict, timeout=10000):
        """
        Logs into Amazon using provided credentials.

        Args:
            email (str): User's email address.
            password (str): User's password.
            selectors (dict): Dictionary with the required CSS selectors.
            timeout (int): Max wait time per step (in ms).
        """
        try:
            # Fill email
            self.page.wait_for_selector(selectors["email"], timeout=timeout)
            self.page.wait_for_timeout(500)
            self.page.fill(selectors["email"], email)
            logger.info("📧 Email entered.")

            # Click 'Continue' button
            self.wait_for_clickable_and_click(selectors["continue"], timeout)

            # Fill password
            self.page.wait_for_selector(selectors["password"], timeout=timeout)
            self.page.wait_for_timeout(500)
            self.page.fill(selectors["password"], password)
            logger.info("🔒 Password entered.")

            # Submit login form
            self.wait_for_clickable_and_click(selectors["submit"], timeout)

            logger.info("✅ Login process completed.")

        except Exception as e:
            logger.exception(f"❌ Login failed due to an error: {e}")


    def verify_url_contains(self, expected_partial_url, timeout=5000):
        """
        Waits up to `timeout` ms for the current URL to contain a specific string.

        Returns:
        - True if the expected URL fragment is found
        - False otherwise
        """
        for _ in range(timeout // 500):
            if expected_partial_url in self.page.url:
                logger.info(f"Expected URL reached: {self.page.url}")
                return True
            self.page.wait_for_timeout(500)

        logger.warning(
            f"Expected URL fragment '{expected_partial_url}' not found. Current URL: {self.page.url}"
        )
        return False

    def open_page(self, url):
        """
        Navigates to the given URL using the Playwright page instance.

        Parameters:
        - url (str): The target URL to navigate to.
        """
        try:
            self.page.goto(url)
            logger.info(f"Navigated to URL: {url}")
        except Exception as e:
            logger.error(f"Failed to navigate to {url}: {e}")
            raise

    def get_visible_text(self, selector: str, timeout=5000) -> str:
        """
        Returns the visible text content of an element, including nested children.

        Args:
            selector (str): The CSS selector of the element.
            timeout (int): Max time to wait for the element (ms).

        Returns:
            str: The visible text (stripped), or empty string if not found.
        """
        try:
            self.page.wait_for_selector(selector, timeout=timeout)
            element = self.page.locator(selector)
            raw_text = element.inner_text().strip()

            # Elimina saltos de línea y múltiples espacios
            cleaned_text = " ".join(raw_text.split())

            # Normaliza caracteres unicode (acentos, etc.)
            normalized_text = unicodedata.normalize("NFC", cleaned_text)

            logger.info(f"Text found in {selector!r}: {normalized_text!r}")
            return normalized_text

        except Exception as e:
            logger.warning(f"Could not retrieve text from {selector}: {e}")
            return ""
        

    def validate_login(self, selector: str) -> bool:
        """
        Validates whether the login was successful by checking the post-login account label.

        Args:
            utils (PlaywrightUtils): Utility class for Playwright actions.

        Returns:
            bool: True if login is successful, False otherwise.
        """
        
        label = self.get_visible_text(selector=selector)

        # Clean Code: simple rule – if label says "Hola" but not "identifícate", user is logged in
        if "Hola" in label and "identifícate" not in label.lower():
            logger.info(f"✅ Login confirmed. Label now shows: {label}")
            return True

        logger.error(f"❌ Login failed. Still showing: {label}")
        return False

    def click_hamburger_option(self, option_text: str, timeout=5000):
        """
        Clicks an item from the Amazon hamburger menu using a dynamic selector.

        Args:
            option_text (str): The visible text of the menu item (e.g., "Electrónicos").
            timeout (int): Maximum wait time in milliseconds.
        """ 
        logger.info(f"Clicking on the hamburger menu option: {option_text}")
        selector = f'a.hmenu-item >> text="{option_text}"'
        logger.info(f"Selector: {selector}")
        self.wait_for_clickable_and_click(selector, timeout)

