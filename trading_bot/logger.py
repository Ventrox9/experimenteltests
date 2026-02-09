import logging
import os
from datetime import datetime

def setup_logger(name='trading_bot', log_file='trading_bot.log', level=logging.INFO):
    """Function to setup as many loggers as you want"""

    # Create logs directory if it doesn't exist
    if not os.path.exists('logs'):
        os.makedirs('logs')

    log_path = os.path.join('logs', log_file)

    formatter = logging.Formatter('%(asctime)s %(levelname)s %(module)s %(funcName)s %(message)s')

    handler = logging.FileHandler(log_path)
    handler.setFormatter(formatter)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Avoid adding handlers multiple times if the logger is already configured
    if not logger.handlers:
        logger.addHandler(handler)
        logger.addHandler(console_handler)

    return logger

# Create a default logger instance
logger = setup_logger()
