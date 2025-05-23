import logging
import os

# Ensure the logs directory exists
os.makedirs("logs", exist_ok=True)

# Basic logger configuration
logging.basicConfig(
    filename="logs/automation.log",
    filemode="a",  # Append mode
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

# Create a logger object that can be imported in any module
logger = logging.getLogger("amazon_automation")
