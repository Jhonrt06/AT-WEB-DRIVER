from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from automation.test_cases.buy_bot import BuyBot
from config.settings import Settings
import traceback

# Create a FastAPI router instance for organizing endpoints
router = APIRouter()

# -------------------- Request and Response Models --------------------

class RunBotRequest(BaseModel):
    """
    Request model for triggering the BuyBot automation flow.
    
    Attributes:
        email (str): Amazon login email.
        password (str): Amazon login password.
        headless (bool): Whether to run the browser in headless mode (default: True).
    """
    email: str
    password: str
    headless: bool = True

class RunBotResponse(BaseModel):
    """
    Response model returned after attempting to run the bot.

    Attributes:
        success (bool): Indicates whether the bot ran successfully.
        message (str): Informational or error message.
    """
    success: bool
    message: str

# -------------------- Endpoint Implementation --------------------

@router.post("/run-bot", response_model=RunBotResponse)
def run_bot(request: RunBotRequest):
    """
    POST endpoint to trigger the automated purchase bot.

    This endpoint receives user credentials and optional headless mode,
    configures the settings, instantiates the BuyBot class, and runs the 
    full purchase flow automation.

    Args:
        request (RunBotRequest): Request body containing login credentials and settings.

    Returns:
        RunBotResponse: A success flag and descriptive message.

    Raises:
        HTTPException: If the bot fails during execution, returns a 500 error with detail.
    """
    try:
        # Load default settings and override headless flag from request
        settings = Settings()
        settings.headless = request.headless

        # Instantiate the BuyBot with user-provided credentials and settings
        bot = BuyBot(
            email=request.email,
            password=request.password,
            headless=request.headless,
            url=settings.amazon_url
        )

        # Run the automation flow (e.g., login, search, add to cart)
        bot.run_purchase_flow()

        # Return a success response if no errors occurred
        return RunBotResponse(success=True, message="Purchase flow completed successfully.")
    
    except Exception as e:
        # Print full traceback to console for debugging
        traceback.print_exc()
        
        # Return a 500 error response with a detailed message
        raise HTTPException(status_code=500, detail=f"Bot execution failed: {str(e)}")
