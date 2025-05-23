from automation.test_cases.comprar_bot import ComprarBot

if __name__ == "__main__":
    bot = ComprarBot(email="tu_correo", password="tu_contraseña")
    bot.abrir_amazon()
