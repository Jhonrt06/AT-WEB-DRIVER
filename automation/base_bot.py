import tempfile
from playwright.sync_api import sync_playwright


class BaseBot:
    """
    Base class that manages the Playwright browser lifecycle.

    This class uses a persistent browser context created in a temporary
    directory to ensure session isolation across runs. It can be used
    with a `with` statement to automatically handle setup and teardown.

    Attributes:
        headless (bool): Whether the browser should run in headless mode.
        temp_profile (str): Path to the temporary browser user data directory.
        browser: Playwright persistent browser context.
        page: Active page used for automation.
    """

    def __init__(self, headless):
        """
        Initializes the BaseBot with the headless setting.

        Args:
            headless (bool): Whether the browser should run headlessly.
        """
        self.headless = headless

    def __enter__(self):
        """
        Starts Playwright and launches a Chromium browser with a persistent context.

        Returns:
            BaseBot: The current instance with initialized browser and page.
        """
        # Start Playwright
        self.p = sync_playwright().start()

        # Create a temporary user data directory for browser session
        self.temp_profile = tempfile.mkdtemp()

        # Launch browser with persistent context using the temporary profile
        self.browser = self.p.chromium.launch_persistent_context(
            user_data_dir=self.temp_profile,
            headless=self.headless,
            viewport={"width": 1280, "height": 800},
            user_agent=(
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/115.0.0.0 Safari/537.36"
            ),
            extra_http_headers={
                "Accept-Language": "es-MX,es;q=0.9",  # Simulate Mexican locale
            }
        )

        # Use existing page if available; otherwise create a new one
        self.page = (
            self.browser.pages[0]
            if self.browser.pages
            else self.browser.new_page()
        )

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Closes the browser and stops the Playwright instance upon exit.

        Args:
            exc_type: Exception type (if any).
            exc_val: Exception value (if any).
            exc_tb: Traceback (if any).
        """
        self.browser.close()
        self.p.stop()
