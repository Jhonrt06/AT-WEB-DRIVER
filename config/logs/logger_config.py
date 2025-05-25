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

# File handler (starts clean each time)
file_handler = logging.FileHandler(LOG_FILE_PATH, mode="w", encoding="utf-8")
file_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))

# Avoid duplicate handlers
if not logger.handlers:
    logger.addHandler(file_handler)

# Disable propagation to root logger
logger.propagate = False
