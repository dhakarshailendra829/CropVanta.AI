import logging
import sys
from logging.handlers import RotatingFileHandler
import os

if not os.path.exists("logs"): os.makedirs("logs")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
        RotatingFileHandler("logs/app.log", maxBytes=10**6, backupCount=3) 
    ]
)

def get_logger(name: str):
    return logging.getLogger(name)