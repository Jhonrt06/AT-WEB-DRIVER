from fastapi import FastAPI
from api.routes.bot_routes import router as bot_router
from config.settings import Settings
import uvicorn
# from automation.test_cases.buy_bot import BuyBot

# Load settings from .env using your Settings class
settings = Settings()

# Initialize FastAPI app
app = FastAPI(
    title="Amazon Purchase Bot API",
    description="API for automating Amazon purchase flow using Playwright",
    version="1.0.0"
)

# Register the route
app.include_router(bot_router, prefix="/api", tags=["Bot Automation"])

# Optional: for development use only (use `uvicorn main:app` instead in prod)
if __name__ == "__main__":
    uvicorn.run("main:app", host=settings.api_host, port=settings.api_port, reload=True)
