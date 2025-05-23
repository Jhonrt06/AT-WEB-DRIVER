from config.settings import Settings

# Crear una instancia de la clase Settings
settings = Settings()

# Imprimir los valores obtenidos desde .env
print("URL de Amazon:", settings.amazon_url)
print("¿Modo headless?:", settings.headless)
