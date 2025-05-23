from config.settings import Settings
from automation.base_bot import BaseBot

# Cargar variables desde .env
settings = Settings()

# Usar BaseBot para abrir navegador y navegar a Amazon
with BaseBot(headless=False) as bot:
    page = bot.page
    page.goto(settings.amazon_url)
    print("✅ Se abrió Amazon correctamente.")
    input("Presiona ENTER para cerrar el navegador...")
