from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from automation.test_cases.buy_bot import BuyBot
from config.settings import Settings
import traceback  # 👈 necesario para imprimir el error completo

router = APIRouter()

class RunBotRequest(BaseModel):
    email: str
    password: str
    headless: bool = True

class RunBotResponse(BaseModel):
    success: bool
    message: str

@router.post("/run-bot", response_model=RunBotResponse)
def run_bot(request: RunBotRequest):
    try:
        settings = Settings()
        settings.headless = request.headless

        bot = BuyBot(
            email=request.email,
            password=request.password,
            headless=request.headless,
            url=settings.amazon_url
        )
        bot.run_purchase_flow()

        return RunBotResponse(success=True, message="Purchase flow completed successfully.")
    
    except Exception as e:
        traceback.print_exc()  # imprime todo el error en consola
        raise HTTPException(status_code=500, detail=f"Bot execution failed: {str(e)}")
