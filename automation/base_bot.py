from playwright.sync_api import sync_playwright

class BaseBot:
    """
    Base class that manages the browser lifecycle using Playwright.
    It can run in headless or headed mode depending on the configuration.
    """

    def __init__(self, headless=True):
        self.headless = headless

    def __enter__(self):
        self.p = sync_playwright().start()
        self.browser = self.p.chromium.launch(headless=self.headless)
        self.context = self.browser.new_context(
    user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
)
        self.page = self.context.new_page()
        return self  # Returns the object to use self.page

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.context.close()
        self.browser.close()
        self.p.stop()
