import os
import logging
from datetime import datetime

# Generate log file name with timestamp
LOG_FILE = f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"

# Define logs directory path
log_dir = os.path.join(os.getcwd(), "logs")

# Create the logs folder if it doesn't exist
os.makedirs(log_dir, exist_ok=True)

# Full path of the log file inside logs folder
LOG_FILE_PATH = os.path.join(log_dir, LOG_FILE)

# Setup logging configuration
logging.basicConfig(
    filename=LOG_FILE_PATH,
    format='[%(asctime)s] %(lineno)d %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


