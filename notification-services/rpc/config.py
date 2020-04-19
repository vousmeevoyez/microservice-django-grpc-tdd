"""
    Configuration
    ______________
    define all configuration used on provider
"""
import os

ENVIRONMENT = os.getenv("ENVIRONMENT")
TELEGRAM = {
    "TOKEN": os.getenv("TELEGRAM_TOKEN"),
    "CHAT_ID": os.getenv("TELEGRAM_CHAT_ID")
}
