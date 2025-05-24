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
        logger.info(f"🔍 Waiting for element {selector!r} to be clickable...")

        try:
            locator = self.page.locator(selector)

            # Espera explícita hasta que esté visible
            self.page.wait_for_timeout(1000)  # Da un respiro a la carga
            locator.wait_for(state="attached", timeout=timeout)
            locator.wait_for(state="visible", timeout=timeout)

            # Scrollea y espera estabilidad
            locator.scroll_into_view_if_needed()
            self.page.wait_for_timeout(500)

            if locator.is_enabled():
                locator.click()
                logger.info(f"✅ Clicked on {selector}")
            else:
                logger.warning(f"⚠️ {selector} is visible but not enabled.")

        except Exception as e:
            logger.error(f"❌ Failed to click '{selector}': {e}")

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


    def click_by_exact_text(self, css_selector: str, exact_text: str, timeout=5000) -> bool:
        """
        Clicks the first element matching the CSS selector and exact visible text.

        Args:
            css_selector (str): Base CSS selector (e.g., 'a.hmenu-item').
            exact_text (str): Exact visible text to match (e.g., 'Electrónicos').
            timeout (int): Max wait time (ms).

        Returns:
            bool: True if click succeeded, False otherwise.
        """
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
        """
        Clicks the first visible hamburger menu item matching the exact label.
        If normal click fails due to visual obstruction, retries with force=True.

        Args:
            label (str): Visible text of the menu item (e.g., "Televisión y Video").
            timeout (int): Max wait time (ms).

        Returns:
            bool: True if the click succeeds, False otherwise.
        """
        try:
            self.page.wait_for_selector("#hmenu-content", timeout=timeout)
            locator = self.page.locator("#hmenu-content a.hmenu-item").filter(
                has_text=label
            )

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
        """
        Scrolls and clicks a visible button/span/link block with exact text.

        Args:
            label (str): Visible text to match (e.g., 'DE 48" A 55"').

        Returns:
            bool: True if the click succeeded, False otherwise.
        """
        try:
            self.page.wait_for_timeout(1000)
            locator = self.page.locator("button, a, span, div").filter(has_text=label)
            locator.first.scroll_into_view_if_needed()
            locator.first.click()
            logger.info(f'✅ Clicked element with label: "{label}"')
            return True
        except Exception as e:
            logger.error(f'❌ Failed to click element with label "{label}": {e}')
            return False

    def click_first_product(self) -> bool:
        """
        Clicks the first product in the visible product carousel.
        Logs the product title before clicking.
        
        Returns:
            bool: True if the product was clicked successfully, False otherwise.
        """
        try:
            selector = "li.octopus-pc-item"
            first_product = self.page.locator(selector).first

            if not first_product.is_visible():
                self.page.evaluate("window.scrollTo(0, 0)")
                self.page.wait_for_timeout(500)
                first_product.evaluate(
                    "(el) => el.scrollIntoView({ behavior: 'smooth', block: 'center' })"
                )
                self.page.wait_for_timeout(1000)

            # Extraer texto visible dentro del producto (por ejemplo, h2, span o p)
            product_text = first_product.inner_text().strip().split("\n")[0]

            # Click
            first_product.click()
            logger.info(f'✅ Clicked first product: "{product_text}"')
            return True

        except Exception as e:
            logger.error(f"❌ Failed to click the first product: {e}")
            return False
        
    def confirm_add_to_cart(self, timeout=5000) -> bool:
        """
        Verifies if the product was successfully added to the cart.

        Strategies:
        - Checks for a cart count badge (like #nav-cart-count)
        - Looks for success messages
        - Logs the outcome
        """
        try:
            # Opción 1: Verifica si el contador del carrito incrementó
            cart_count = self.page.locator("#nav-cart-count")
            if cart_count.is_visible(timeout=timeout):
                count_text = cart_count.inner_text().strip()
                if count_text.isdigit() and int(count_text) > 0:
                    logger.info(f"🛒 Product added to cart. Cart count: {count_text}")
                    return True

            # Opción 2: Verifica un mensaje típico
            success_msg = self.page.locator('text="Agregado al carrito"')
            if success_msg.is_visible(timeout=timeout):
                logger.info("✅ Product added to cart - success message found.")
                return True

            logger.warning("⚠️ Could not confirm product was added to cart.")
            return False

        except Exception as e:
            logger.error(f"❌ Error verifying cart addition: {e}")
            return False

    def close_warranty_popup(self, timeout=3000):
        """
        Closes the Amazon warranty popup if it appears, by clicking outside its bounds.

        Returns:
            bool: True if closed successfully, False if it wasn't open or couldn't be closed.
        """
        popup_selector = "#attach-warranty-pane"

        try:
            popup = self.page.locator(popup_selector)

            if not popup.is_visible(timeout=timeout):
                logger.info("✅ Warranty popup not visible.")
                return False

            # Obtener posición y tamaño del popup
            box = popup.bounding_box()
            if not box:
                logger.warning("⚠️ Could not retrieve bounding box of warranty popup.")
                return False

            # Calcular una coordenada fuera del área del popup
            x = max(box["x"] - 50, 0)
            y = max(box["y"] - 50, 0)

            # Click fuera del popup
            self.page.mouse.click(x, y)
            self.page.wait_for_timeout(800)

            logger.info(f"🖱️ Clicked outside warranty popup at ({x}, {y})")
            return True

        except Exception as e:
            logger.error(f"❌ Failed to close warranty popup: {e}")
            return False
