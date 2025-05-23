from automation.test_cases.comprar_bot import BuyBot

if __name__ == "__main__":
    bot = BuyBot(email="project.otua1@gmail.com", password="esunaprueba")
    bot.run_purchase_flow()
