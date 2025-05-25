import tempfile
from playwright.sync_api import sync_playwright


class BaseBot:
    """
    Base class that manages the browser lifecycle using Playwright.
    It runs with a fresh persistent context on each execution,
    ensuring session isolation and clean automation.
    """

    def __init__(self, headless=True):
        self.headless = headless

    def __enter__(self):
        self.p = sync_playwright().start()

        # Create a unique temporary profile for this session
        self.temp_profile = tempfile.mkdtemp()

        # Launch browser with persistent context (clean session)
        self.browser = self.p.chromium.launch_persistent_context(
            user_data_dir=self.temp_profile,
            headless=False,
            viewport={"width": 1280, "height": 800},
            user_agent=(
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/115.0.0.0 Safari/537.36"
            ),
        )

        self.page = (
            self.browser.pages[0]
            if self.browser.pages
            else self.browser.new_page()
        )
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.browser.close()
        self.p.stop()
