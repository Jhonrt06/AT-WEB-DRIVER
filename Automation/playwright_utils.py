"""
Clase PlaywrightUtils
Contiene métodos reutilizables para interactuar con páginas web usando Playwright.

Uso típico:
    utils = PlaywrightUtils(page)
    utils.rellenar_input("#campo", "texto")
    utils.esperar_y_clickear("#boton")
"""


class PlaywrightUtils:
    def __init__(self, page):
        """
        Inicializa la utilidad con una página de Playwright.

        Parámetros:
        - page: objeto Page creado por Playwright (bot.page)
        """
        self.page = page

    def esperar_y_clickear(self, selector, timeout=10000):
        """
        Espera a que el elemento esté disponible y hace clic.

        Parámetros:
        - selector: selector CSS del botón o enlace
        - timeout: tiempo máximo de espera (milisegundos)
        """
        self.page.wait_for_selector(selector, timeout=timeout)
        self.page.click(selector)

    def rellenar_input(self, selector, texto, timeout=10000):
        """
        Espera un campo de texto y lo rellena con el texto dado.

        Parámetros:
        - selector: selector CSS del campo input
        - texto: texto a escribir en el campo
        - timeout: tiempo máximo de espera
        """
        self.page.wait_for_selector(selector, timeout=timeout)
        self.page.fill(selector, texto)

    def esperar_texto(self, texto_esperado, timeout=10000):
        """
        Espera brevemente y verifica si cierto texto está en la página.

        Parámetros:
        - texto_esperado: texto que esperamos encontrar
        - timeout: tiempo de espera total

        Retorna:
        - True si el texto está en la página, False si no
        """
        self.page.wait_for_timeout(1000)
        return texto_esperado in self.page.content()

    def login(self, email, password, selectors, timeout=10000):
        """
        Realiza login genérico usando los selectores indicados.

        Parámetros:
        - email: correo electrónico
        - password: contraseña
        - selectors: diccionario con selectores CSS
        """
        print("Estas en login function")
        # self.rellenar_input(selectors["email"], email, timeout)
        # self.esperar_y_clickear(selectors["continuar"], timeout)
        # self.rellenar_input(selectors["password"], password, timeout)
        # self.esperar_y_clickear(selectors["submit"], timeout)

    def elemento_visible(self, selector, timeout=5000):
        """
        Verifica si un elemento es visible en la página dentro del tiempo dado.

        Retorna:
        - True si aparece el selector
        - False si no (Timeout)
        """
        try:
            self.page.wait_for_selector(selector, timeout=timeout, state="visible")
            logger.info(f"Elemento visible: {selector}")
            return True
        except TimeoutError:
            logger.warning(f"Elemento NO visible: {selector}")
            return False