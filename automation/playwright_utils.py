from playwright.sync_api import TimeoutError
from config.logs.logger_config import logger


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

    def wait_and_click(self, selector, timeout=10000):
        """
        Waits for the element to be available and clicks it.

        Parameters:
        - selector: CSS selector of the button or link
        - timeout: maximum wait time in milliseconds
        """
        self.page.wait_for_selector(selector, timeout=timeout)
        self.page.click(selector)

    def fill_input(self, selector, text, timeout=10000):
        """
        Waits for a text field to be available and fills it with the given text.

        Parameters:
        - selector: CSS selector of the input field
        - text: text to fill in the field
        - timeout: maximum wait time
        """
        self.page.wait_for_selector(selector, timeout=timeout)
        self.page.fill(selector, text)

    def wait_for_text(self, expected_text, timeout=10000):
        """
        Waits briefly and checks if a specific text appears on the page.

        Parameters:
        - expected_text: the text we expect to find
        - timeout: total wait time

        Returns:
        - True if the text is on the page, False otherwise
        """
        self.page.wait_for_timeout(1000)
        return expected_text in self.page.content()

    def login(self, email, password, selectors, timeout=10000):
        """
        Performs a generic login using the given selectors.

        Parameters:
        - email: user's email address
        - password: user's password
        - selectors: dictionary of CSS selectors
        """
        print("You are in the login function")

    def verify_element(self, selector, timeout=5000):
        """
        Checks if an element is visible on the page within the given time.

        Returns:
        - True if the selector is found
        - False if not (Timeout)
        """
        try:
            self.page.wait_for_selector(selector, timeout=timeout, state="visible")
            logger.info(f"Element is visible: {selector}")
            return True
        except TimeoutError:
            logger.warning(f"Element NOT visible: {selector}")
            return False

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
