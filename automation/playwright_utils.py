from config.logs.logger_config import logger
from functools import wraps
from playwright.sync_api import TimeoutError
import unicodedata
from functools import wraps

# Constant for locating all potential clickable HTML elements
ALL_CLICKABLE_ELEMENTS = "button, a, span, div"


def log_step(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        logger.info(f"Starting: {func.__name__}")
        self.page.wait_for_timeout(
            1000
        )  # Added delay before executing the function
        result = func(self, *args, **kwargs)
        logger.info(f"Finished: {func.__name__}")
        return result
    return wrapper

def safe_action(default=False):
    def decorator(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            try:
                return func(self, *args, **kwargs)
            except TimeoutError as e:
                logger.error(f"Timeout: {func.__name__} - {e}")
            except Exception as e:
                logger.exception(f"Unexpected error in {func.__name__}: {e}")
            return default
        return wrapper
    return decorator

class PlaywrightUtils:
    """
    A utility class to encapsulate common web interaction operations using Playwright.

    Attributes:
        page: A Playwright page object for performing browser interactions.

    Example:
        utils = PlaywrightUtils(page)
        utils.open_page("https://example.com")
        utils.fill_input("#username", "admin")
        utils.wait_for_clickable_and_click("#submit")
    """

    def __init__(self, page):
        """
        Initializes the PlaywrightUtils class.

        Args:
            page: The Playwright page object to use for interactions.
        """
        self.page = page

    # --------------------- Navigation ---------------------

    @log_step
    def open_page(self, url) -> None:
        """
        Navigates the browser to the specified URL.

        Args:
            url (str): The web address to open.
        """
        try:
            # Navigate to the target URL
            self.page.goto(url)

            # Log successful navigation
            logger.info(f"Navigated to URL: {url}")

        except Exception as error:
            # Log the error and re-raise it to ensure it can be handled at a higher level
            logger.error(f"Failed to navigate to {url}: {error}")
            raise

    # --------------------- Element interaction ---------------------

    @log_step
    def wait_for_clickable_and_click(
        self, selector: str, timeout=10000
    ) -> None:
        """
        Waits until the specified element is attached, visible, and enabled, then clicks it.

        Args:
            selector (str): CSS selector of the element to click.
            timeout (int): Time to wait before timeout (milliseconds).
        """

        logger.debug(f"Waiting for element {selector!r} to be clickable...")

        try:
            # Create a locator for the target element
            locator = self.page.locator(selector)

            # Wait until the element is in the DOM and visible
            locator.wait_for(state="attached", timeout=timeout)
            locator.wait_for(state="visible", timeout=timeout)

            # Scroll the element into view to ensure it is not obstructed
            locator.scroll_into_view_if_needed()
            self.page.wait_for_timeout(
                500
            )  # Small buffer to allow visual stabilization

            # If the element is enabled (interactable), click it
            if locator.is_enabled():
                locator.click()
                logger.info(f"Clicked on {selector}")
            else:
                logger.warning(f"{selector} is visible but not enabled.")
                raise RuntimeError(f"Element {selector} is not enabled for clicking.")

        except Exception as error:
            # Log any errors encountered while trying to interact with the element
            logger.error(f"Failed to click '{selector}': {error}")

    @log_step
    @safe_action(default=False)
    def click_by_exact_text(
        self, css_selector: str, exact_text: str, timeout=5000
    ) -> bool:
        """
        Clicks the first element that matches a CSS selector and exact visible text.

        Args:
            css_selector (str): CSS selector for locating the elements.
            exact_text (str): Exact text the element must contain.
            timeout (int): Timeout in milliseconds.

        Returns:
            bool: True if the click was successful, False otherwise.
        """

        # Wait for the base selector to be available in the DOM
        self.page.wait_for_selector(css_selector, timeout=timeout)

        # Filter elements by exact visible text
        locator = self.page.locator(css_selector).filter(
            has_text=exact_text
        )

        # Click the first matching element
        locator.first.click()

        # Log success
        logger.info(f'Clicked element with exact text: "{exact_text}"')
        return True


    @log_step
    @safe_action(default=False)
    def click_hamburger_item_by_label(self, label: str, timeout=5000) -> bool:
        """
        Clicks an item inside a hamburger menu based on its label text.

        Args:
            label (str): Text label of the menu item.
            timeout (int): Timeout in milliseconds.

        Returns:
            bool: True if the click was successful, False otherwise.
        """

        # Wait for the hamburger menu container to be visible
        self.page.wait_for_selector("#hmenu-content", timeout=timeout)

        # Filter all menu items inside the container that match the exact label
        locator = self.page.locator("#hmenu-content a.hmenu-item").filter(
            has_text=label
        )
        try:
            # Click the first matching item
            locator.first.click(timeout=timeout)

        except Exception as error:
            # If normal click fails, try using force=True to bypass visual obstructions
            logger.warning(
                f'Normal click failed for "{label}", retrying with force=True: {error}'
            )
            locator.first.click(timeout=timeout, force=True)
            logger.info(f'Forced click succeeded for "{label}"')

    @log_step
    @safe_action(default=False)
    def click_text_block_by_label(self, label: str, timeout=5000) -> bool:
        """
        Clicks any block element (button, div, span, etc.) that contains the specified text.

        Args:
            label (str): Text to match inside the element.
            timeout (int): Timeout in milliseconds.

        Returns:
            bool: True if the click was successful, False otherwise.
        """

            # Locate the first matching element among all standard clickable tags
        locator = self.page.locator(ALL_CLICKABLE_ELEMENTS).filter(
            has_text=label
        )

        # Scroll the element into view if necessary
        locator.first.scroll_into_view_if_needed()

        # Attempt to click the element
        locator.first.click()
        logger.info(f'Clicked element with label: "{label}"')
        return True

    # --------------------- Product and cart actions ---------------------

    @log_step
    @safe_action(default=False)
    def click_first_product(self) -> bool:

        """
        Clicks the first product in a product listing or carousel.

        Returns:
            bool: True if successful, False otherwise.
        """

        # Define the selector for product items (carousel or grid)
        selector = "li.octopus-pc-item"
        first_product = self.page.locator(selector).first

        # If the product is not immediately visible, scroll to top and bring it into view
        if not first_product.is_visible():
            self.page.evaluate("window.scrollTo(0, 0)")
            self.page.wait_for_timeout(500)
            first_product.evaluate(
                "(el) => el.scrollIntoView({ behavior: 'smooth', block: 'center' })"
            )
            self.page.wait_for_timeout(1000)

        # Extract product name (first line of text)
        product_text = first_product.inner_text().strip().split("\n")[0]

        # Click the product
        first_product.click()
        logger.info(f'Clicked first product: "{product_text}"')
        return True

    @safe_action(default=False)
    def confirm_add_to_cart(self, timeout=5000) -> bool:
        """
        Confirms if an item has been added to the shopping cart.

        Args:
            timeout (int): Timeout in milliseconds.

        Returns:
            bool: True if the cart contains items, False otherwise.
        """

        # Strategy 1: Check the cart item count badge
        cart_count = self.page.locator("#nav-cart-count")
        if cart_count.is_visible(timeout=timeout):
            count_text = cart_count.inner_text().strip()
            if count_text.isdigit() and int(count_text) > 0:
                logger.info(
                    f"🛒 Product added to cart. Cart count: {count_text}"
                )
                return True

        # Strategy 2: Check for a confirmation message
        success_msg = self.page.locator('text="Agregado al carrito"')
        if success_msg.is_visible(timeout=timeout):
            logger.info("Product added to cart - success message found.")
            return True

        # Neither method confirmed the product was added
        logger.warning("Could not confirm product was added to cart.")
        return False

 # --------------------- Auth and validation ---------------------

    @log_step
    def login(
        self, email: str, password: str, selectors: dict, timeout=10000
    ) -> None:
        """
        Automates the login process by filling in credentials and submitting the form.

        Args:
            email (str): User email.
            password (str): User password.
            selectors (dict): Dictionary of field selectors (email, password, continue, submit).
            timeout (int): Timeout in milliseconds.
        """
        try:
            # Wait for the email field and fill it
            self.page.wait_for_selector(selectors["email"], timeout=timeout)
            self.page.wait_for_timeout(500)
            self.page.fill(selectors["email"], email)
            logger.info("📧 Email entered.")

            # Click the "Continue" button
            self.wait_for_clickable_and_click(selectors["continue"], timeout)

            # Wait for the password field and fill it
            self.page.wait_for_selector(selectors["password"], timeout=timeout)
            self.page.wait_for_timeout(500)
            self.page.fill(selectors["password"], password)
            logger.info("Password entered.")

            # Click the "Submit" button to complete login
            self.wait_for_clickable_and_click(selectors["submit"], timeout)
            logger.info("Login process completed.")

        except Exception as error:
            # Log and raise any error that prevents login completion
            logger.exception(f"Login failed due to an error: {error}")

    @log_step
    @safe_action(default=False)
    def validate_login(self, selector: str) -> bool:
        """
        Validates that login was successful by checking the greeting label.

        Args:
            selector (str): Selector for the greeting label.

        Returns:
            bool: True if login is confirmed, False otherwise.
        """
        # Extract the visible text from the greeting label
        label = self.get_visible_text(selector=selector)

        # Check that the label starts with "Hola" and does not include "identifícate"
        # This implies the user is logged in
        if (
            label.strip().startswith("Hola")
            and "identifícate" not in label.lower()
        ):
            logger.info(f"Login confirmed. Label now shows: {label}")
            return True

        # If conditions aren't met, assume login failed
        logger.error(f"Login failed. Still showing: {label}")
        return False

    # --------------------- Visual Utilities ---------------------

    @safe_action("")
    def get_visible_text(self, selector: str, timeout=5000) -> str:
        """
        Retrieves and normalizes the visible text content of a DOM element.

        Args:
            selector (str): CSS selector of the target element.
            timeout (int): Timeout in milliseconds.

        Returns:
            str: Cleaned and normalized visible text, or empty string if failed.
        """
        try:
            # Wait for the element to appear in the DOM
            self.page.wait_for_selector(selector, timeout=timeout)

            # Get a locator reference to the element
            element = self.page.locator(selector)

            # Extract raw visible text and remove surrounding whitespace
            raw_text = element.inner_text().strip()

            # Normalize spaces and remove line breaks
            cleaned_text = " ".join(raw_text.split())

            # Normalize unicode characters (e.g., accents)
            normalized_text = unicodedata.normalize("NFC", cleaned_text)

            # Log and return the final cleaned text
            logger.info(f"Text found in {selector!r}: {normalized_text!r}")
            return normalized_text

        except Exception as error:
            # Log warning and return empty string if extraction fails
            logger.exception(f"Could not retrieve text from {selector}: {error}")
            return ""

    @log_step
    @safe_action(default=False)
    def close_warranty_popup(self, timeout=3000) -> bool:
        """
        Attempts to close the warranty offer popup by clicking outside of its bounds.

        Args:
            timeout (int): Timeout in milliseconds.

        Returns:
            bool: True if the popup was closed, False otherwise.
        """
        popup_selector = "#attach-warranty-pane"


        # Locate the popup element
        popup = self.page.locator(popup_selector)

        # If popup is not visible, nothing to close
        if not popup.is_visible(timeout=timeout):
            logger.info("Warranty popup not visible.")
            return False

        # Get position and dimensions of the popup
        box = popup.bounding_box()
        if not box:
            logger.warning(
                "Could not retrieve bounding box of warranty popup."
            )
            return False

        # Compute a point outside the popup area
        x = max(box["x"] - 50, 0)
        y = max(box["y"] - 50, 0)

        # Simulate a mouse click outside the popup to dismiss it
        self.page.mouse.click(x, y)
        self.page.wait_for_timeout(800)
        logger.info(f"Clicked outside warranty popup at ({x}, {y})")
        return True
