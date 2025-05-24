from playwright.sync_api import TimeoutError
from config.logs.logger_config import logger
import unicodedata

# Constants
ALL_CLICKABLE_ELEMENTS = "button, a, span, div"

class PlaywrightUtils:
    """
    PlaywrightUtils class
    Contains reusable methods for interacting with web pages using Playwright.

    Typical usage:
        utils = PlaywrightUtils(page)
        utils.fill_input("#field", "text")
        utils.wait_for_clickable_and_click("#button")
    """

    def __init__(self, page):
        """Initializes the PlaywrightUtils class with the given Playwright page object."""
        self.page = page

    # --------------------- Navigation ---------------------

    def open_page(self, url):
        """Navigates to the given URL using the Playwright page instance and logs the action."""
        try:
            self.page.goto(url)
            logger.info(f"Navigated to URL: {url}")
        except Exception as e:
            logger.error(f"Failed to navigate to {url}: {e}")
            raise

    # --------------------- Element interaction ---------------------

    def wait_for_clickable_and_click(self, selector: str, timeout=10000):
        """Waits until the element is attached and visible, then clicks it if enabled."""
        logger.info(f"🔍 Waiting for element {selector!r} to be clickable...")
        try:
            locator = self.page.locator(selector)
            locator.wait_for(state="attached", timeout=timeout)
            locator.wait_for(state="visible", timeout=timeout)
            locator.scroll_into_view_if_needed()
            self.page.wait_for_timeout(500)

            if locator.is_enabled():
                locator.click()
                logger.info(f"✅ Clicked on {selector}")
            else:
                logger.warning(f"⚠️ {selector} is visible but not enabled.")
        except Exception as e:
            logger.error(f"❌ Failed to click '{selector}': {e}")

    def click_by_exact_text(self, css_selector: str, exact_text: str, timeout=5000) -> bool:
        """Clicks the first element that matches the given CSS selector and exact visible text."""
        try:
            self.page.wait_for_selector(css_selector, timeout=timeout)
            locator = self.page.locator(css_selector).filter(has_text=exact_text)
            locator.first.click()
            logger.info(f'✅ Clicked element with exact text: "{exact_text}"')
            return True
        except Exception as e:
            logger.error(f'❌ Could not click element with text "{exact_text}": {e}')
            return False

    def click_hamburger_item_by_label(self, label: str, timeout=5000) -> bool:
        """Clicks an item in the hamburger menu based on the exact label provided."""
        try:
            self.page.wait_for_selector("#hmenu-content", timeout=timeout)
            locator = self.page.locator("#hmenu-content a.hmenu-item").filter(has_text=label)
            logger.info(f'🔍 Trying to click "{label}" from hamburger menu...')
            locator.first.click(timeout=timeout)
            logger.info(f'✅ Clicked menu item: "{label}"')
            return True
        except Exception as e:
            logger.warning(f'⚠️ Normal click failed for "{label}", retrying with force=True: {e}')
            try:
                locator.first.click(timeout=timeout, force=True)
                logger.info(f'✅ Forced click succeeded for "{label}"')
                return True
            except Exception as e_force:
                logger.error(f'❌ Forced click failed for "{label}": {e_force}')
                return False

    def click_text_block_by_label(self, label: str, timeout=5000):
        """Scrolls into view and clicks an element containing the specified text label."""
        try:
            locator = self.page.locator(ALL_CLICKABLE_ELEMENTS).filter(has_text=label)
            locator.first.scroll_into_view_if_needed()
            locator.first.click()
            logger.info(f'✅ Clicked element with label: "{label}"')
            return True
        except Exception as e:
            logger.error(f'❌ Failed to click element with label "{label}": {e}')
            return False

    # --------------------- Product and cart actions ---------------------

    def click_first_product(self) -> bool:
        """Clicks the first visible product item from a carousel or listing on the page."""
        try:
            selector = "li.octopus-pc-item"
            first_product = self.page.locator(selector).first

            if not first_product.is_visible():
                self.page.evaluate("window.scrollTo(0, 0)")
                self.page.wait_for_timeout(500)
                first_product.evaluate("(el) => el.scrollIntoView({ behavior: 'smooth', block: 'center' })")
                self.page.wait_for_timeout(1000)

            product_text = first_product.inner_text().strip().split("\n")[0]
            first_product.click()
            logger.info(f'✅ Clicked first product: "{product_text}"')
            return True

        except Exception as e:
            logger.error(f"❌ Failed to click the first product: {e}")
            return False

    def confirm_add_to_cart(self, timeout=5000) -> bool:
        """Verifies that a product was added to the cart by checking UI indicators."""
        try:
            cart_count = self.page.locator("#nav-cart-count")
            if cart_count.is_visible(timeout=timeout):
                count_text = cart_count.inner_text().strip()
                if count_text.isdigit() and int(count_text) > 0:
                    logger.info(f"🛒 Product added to cart. Cart count: {count_text}")
                    return True

            success_msg = self.page.locator('text="Agregado al carrito"')
            if success_msg.is_visible(timeout=timeout):
                logger.info("✅ Product added to cart - success message found.")
                return True

            logger.warning("⚠️ Could not confirm product was added to cart.")
            return False

        except Exception as e:
            logger.error(f"❌ Error verifying cart addition: {e}")
            return False

    # --------------------- Auth and validation ---------------------

    def login(self, email: str, password: str, selectors: dict, timeout=10000):
        """Performs a login operation using the given credentials and selectors."""
        try:
            self.page.wait_for_selector(selectors["email"], timeout=timeout)
            self.page.wait_for_timeout(500)
            self.page.fill(selectors["email"], email)
            logger.info("📧 Email entered.")

            self.wait_for_clickable_and_click(selectors["continue"], timeout)

            self.page.wait_for_selector(selectors["password"], timeout=timeout)
            self.page.wait_for_timeout(500)
            self.page.fill(selectors["password"], password)
            logger.info("🔒 Password entered.")

            self.wait_for_clickable_and_click(selectors["submit"], timeout)
            logger.info("✅ Login process completed.")

        except Exception as e:
            logger.exception(f"❌ Login failed due to an error: {e}")

    def validate_login(self, selector: str) -> bool:
        """Checks if the login was successful by analyzing the greeting label content."""
        label = self.get_visible_text(selector=selector)
        if label.strip().startswith("Hola") and "identifícate" not in label.lower():
            logger.info(f"✅ Login confirmed. Label now shows: {label}")
            return True

        logger.error(f"❌ Login failed. Still showing: {label}")
        return False

    # --------------------- Visual Utilities ---------------------

    def get_visible_text(self, selector: str, timeout=5000) -> str:
        """Retrieves and normalizes the visible text content of a web element."""
        try:
            self.page.wait_for_selector(selector, timeout=timeout)
            element = self.page.locator(selector)
            raw_text = element.inner_text().strip()
            cleaned_text = " ".join(raw_text.split())
            normalized_text = unicodedata.normalize("NFC", cleaned_text)
            logger.info(f"Text found in {selector!r}: {normalized_text!r}")
            return normalized_text
        except Exception as e:
            logger.warning(f"Could not retrieve text from {selector}: {e}")
            return ""

    def close_warranty_popup(self, timeout=3000):
        """Attempts to close the warranty upsell popup by clicking outside its bounds."""
        popup_selector = "#attach-warranty-pane"
        try:
            popup = self.page.locator(popup_selector)
            if not popup.is_visible(timeout=timeout):
                logger.info("✅ Warranty popup not visible.")
                return False

            box = popup.bounding_box()
            if not box:
                logger.warning("⚠️ Could not retrieve bounding box of warranty popup.")
                return False

            x = max(box["x"] - 50, 0)
            y = max(box["y"] - 50, 0)
            self.page.mouse.click(x, y)
            self.page.wait_for_timeout(800)
            logger.info(f"🖱️ Clicked outside warranty popup at ({x}, {y})")
            return True

        except Exception as e:
            logger.error(f"❌ Failed to close warranty popup: {e}")
            return False
