import logging
import os
from datetime import datetime
import shutil

# Paths
LOG_DIR = "logs"
LOG_FILE_NAME = "automation.log"
LOG_FILE_PATH = os.path.join(LOG_DIR, LOG_FILE_NAME)

# Create logs directory if it doesn't exist
os.makedirs(LOG_DIR, exist_ok=True)

# Backup previous log if it exists
if os.path.exists(LOG_FILE_PATH):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = os.path.join(LOG_DIR, f"automation_{timestamp}.log")
    shutil.move(LOG_FILE_PATH, backup_path)

# Set up logger
logger = logging.getLogger("automation_logger")
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

# File handler
file_handler = logging.FileHandler(LOG_FILE_PATH, mode="w", encoding="utf-8")
file_handler.setFormatter(formatter)

# Console handler
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)

# Avoid duplicate handlers
if not logger.handlers:
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

# Prevent logs from propagating to the root logger
logger.propagate = False
