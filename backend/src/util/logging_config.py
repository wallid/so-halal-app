import logging
import os
from logging.handlers import TimedRotatingFileHandler

LOG_FILE_PATH = "./logs/fastapi_app.log"

# Create logs directory if it doesn't exist
if not os.path.exists(os.path.dirname(LOG_FILE_PATH)):
    os.makedirs(os.path.dirname(LOG_FILE_PATH))

def configure_logging():
    """
    Configures the logging for the FastAPI application to both console and file.
    """
    # Get the root logger
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    # Console handler (StreamHandler)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)

    # File handler (TimedRotatingFileHandler)
    file_handler = TimedRotatingFileHandler(
        LOG_FILE_PATH, when="midnight", interval=1, backupCount=7
    )
    file_handler.setLevel(logging.INFO)

    # Log format for both handlers
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    console_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)

    # Adding handlers to the logger
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    # Disable overly verbose logging for external libraries like uvicorn
    logging.getLogger("uvicorn").setLevel(logging.WARNING)
    logging.getLogger("uvicorn.access").disabled = True

    logger.info("Logging configured to both console and file.")
