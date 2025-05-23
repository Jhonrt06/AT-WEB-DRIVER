from automation.test_cases.comprar_bot import ComprarBot

if __name__ == "__main__":
    bot = ComprarBot(email="project.otua1@gmail.com", password="esunaprueba")
    bot.run_purchase_flow()
