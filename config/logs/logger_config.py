import logging
import os

# Asegúrate de que exista la carpeta de logs
os.makedirs("logs", exist_ok=True)

# Configuración básica del logger
logging.basicConfig(
    filename="logs/automation.log",
    filemode="a",
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

# Crear objeto logger que puedes importar en cualquier archivo
logger = logging.getLogger("amazon_automation")
