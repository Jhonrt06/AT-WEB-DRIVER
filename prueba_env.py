from config.settings import Settings

# Create an instance of the Settings class
settings = Settings()

# Print the values retrieved from the .env file
print("Amazon URL:", settings.amazon_url)
print("Headless mode?:", settings.headless)
