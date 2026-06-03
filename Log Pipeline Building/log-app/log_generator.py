#!/usr/bin/env python3
import logging
import time
import random
from datetime import datetime

# TODO: Configure logging with appropriate format
# Include timestamp, log level, and message
# logging.basicConfig(...)

def generate_logs():
    """
    Generate sample application logs with various severity levels.
    
    TODO: Implement log generation logic
    - Create logs with different levels (INFO, WARNING, ERROR)
    - Include realistic application events
    - Add random delays between logs
    """
    log_messages = [
        ("INFO", "User login successful"),
        ("INFO", "Database connection established"),
        ("WARNING", "High memory usage detected"),
        ("ERROR", "Failed to connect to external API"),
        ("INFO", "Transaction completed successfully"),
    ]
    
    # TODO: Implement the logging loop
    pass

if __name__ == "__main__":
    generate_logs()
# Add this configuration at the top of generate_logs():
logging.basicConfig(
    filename='/home/ubuntu/app.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# In the loop:
for _ in range(20):
    level, message = random.choice(log_messages)
    if level == "INFO":
        logging.info(message)
    elif level == "WARNING":
        logging.warning(message)
    elif level == "ERROR":
        logging.error(message)
    time.sleep(2)
