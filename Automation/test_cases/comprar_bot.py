from automation.base_bot import BaseBot
from automation.playwright_utils import PlaywrightUtils
from config.settings import Settings
from automation.playwright_constants import SELECTORS_AMAZON
from config.logs.logger_config import logger

class ComprarBot:
    """
    Test case: automatización del flujo de compra.
    Contiene métodos para abrir Amazon y hacer login.
    """

    def __init__(self, email, password):
        self.email = email
        self.password = password
        self.settings = Settings()
        # self.headless = self.settings.headless

    def abrir_amazon(self):

        logger.info("Iniciando sesión en Amazon...")
        with BaseBot(headless=False) as bot:
            page = bot.page
            page.goto(self.settings.amazon_url)
            print("✅ Se abrió Amazon correctamente.")
            input("Presiona ENTER para cerrar el navegador...")

    def login_amazon(self):


        logger.info("Iniciando sesión en Amazon...")
        with BaseBot(headless=self.settings.headless) as bot:
            page = bot.page
            page.goto("https://www.amazon.com.mx/ap/signin")

            utils = PlaywrightUtils(page)
            utils.login(
                self.email, self.password, SELECTORS_AMAZON["login_button_home"]
            )

            print("✅ Login completado.")
            input("Presiona ENTER para cerrar el navegador...")
