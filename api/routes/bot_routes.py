from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from automation.test_cases.buy_bot import BuyBot  # Asegúrate de que la ruta sea correcta
from config.settings import Settings

router = APIRouter()

# Pydantic model for request body
class RunBotRequest(BaseModel):
    email: str
    password: str
    headless: bool = True  # opcional, por defecto True

# Pydantic model for response body
class RunBotResponse(BaseModel):
    success: bool
    message: str

@router.post("/run-bot", response_model=RunBotResponse)
def run_bot(request: RunBotRequest):
    try:
        settings = Settings()
        settings.headless = request.headless  # Override headless if needed

        bot = BuyBot(
            email=request.email,
            password=request.password,
            headless=request.headless,
            amazon_url=settings.amazon_url
        )
        bot.run_purchase_flow()

        return RunBotResponse(success=True, message="Purchase flow completed successfully.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Bot execution failed: {e}")
