from config.settings import Settings
from automation.base_bot import BaseBot

# Cargar variables desde .env
settings = Settings()
css_selector = "a.hmenu-item"
exact_text = "Televisión y Video"
# Usar BaseBot para abrir navegador y navegar a Amazon
with BaseBot(headless=False) as bot:
    page = bot.page
    page.goto(settings.amazon_url)
    # try:
    #     page.wait_for_selector(css_selector, timeout=5000)
    input(
        "Press Enter to continue..."
    )  # Pausa para permitir al usuario ver la página
    #     locator = page.locator(css_selector).filter(has_text=exact_text)
    #     locator.first.click()
    #     print(f'✅ Clicked element with exact text: "{exact_text}"')
    #     input("Press Enter to continue...")  # Pausa para permitir al usuario ver la acción
    # except Exception as e:
    #     print(f'❌ Could not click element with text "{exact_text}": {e}')
    page.wait_for_selector("#nav-cart", timeout=5000)
    locator = page.locator("#nav-cart")
    locator.click()
    print('✅ Clicked element with exact text: "Buy Now"')
    input(
        "Press Enter to continue..."
    )  # Pausa para permitir al usuario ver la acción
    page.wait_for_selector(
        "input[name='proceedToRetailCheckout']", timeout=5000
    )
    locator = page.locator("input[name='proceedToRetailCheckout']")
    locator.click()
    input(
        "Press Enter to continue..."
    )  # Pausa para permitir al usuario ver la acción
