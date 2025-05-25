from automation.test_cases.buy_bot import BuyBot
from config.logs.logger_config import logger

if __name__ == "__main__":
    try:
        bot = BuyBot(email="project.otua1@gmail.com", password="esunaprueba")
        bot.run_purchase_flow(product_name="Pantalla 50 pulgadas")
    except Exception as e:
        logger.exception(f"Unhandled error during automation: {e}")
