from dotenv import load_dotenv
import os

# Carga las variables de entorno del archivo .env
load_dotenv()


class Settings:
    """
    Clase que carga y gestiona las variables de entorno del proyecto.

    Esta clase se encarga de leer las variables definidas en el archivo `.env`
    usando la librería `python-dotenv`, y proporciona acceso a ellas de forma segura
    dentro del código.

    Atributos:
    ----------
    amazon_url : str
        URL base del sitio de Amazon que se utilizará en la automatización.

    headless : bool
        Define si el navegador debe ejecutarse en modo invisible (headless)
        o visible (headed). Se espera un valor 'true' o 'false' en formato string.
    """

    def __init__(self):
        self.amazon_url = os.getenv("AMAZON_URL")
        self.headless = os.getenv("HEADLESS", "true").lower() == "true"
