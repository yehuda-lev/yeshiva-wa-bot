import os
from typing import Type
import dotenv


dotenv.load_dotenv()


class Settings:
    """read the settings from .env file"""

    WA_PHONE_ID = os.environ["WA_PHONE_ID"]
    WA_BUSINESS_ID = os.environ["WA_BUSINESS_ID"]
    WA_TOKEN = os.environ["WA_TOKEN"]
    WA_VERIFY_TOKEN = os.environ["WA_VERIFY_TOKEN"]
    WA_PHONE_NUMBER = os.environ["WA_PHONE_NUMBER"]

    APP_ID = os.environ["APP_ID"]
    APP_SECRET = os.environ["APP_SECRET"]

    CALLBACK_URL = os.environ["CALLBACK_URL"]
    WEBHOOK_ENDPOINT = os.environ["WEBHOOK_ENDPOINT"]
    UNDER_MAINTENANCE = os.environ["UNDER_MAINTENANCE"]
    ADMINS = os.environ["WA_ADMINS"]

    FLOW_ID = os.environ["FLOW_ID"]
    FLOW_STATUS = os.environ["FLOW_STATUS"]
    PRIVATE_KEY = os.environ["PRIVATE_KEY"]
    PASSWORD_PRIVATE_KEY = os.environ["PASSWORD_PRIVATE_KEY"]


def get_settings() -> Type[Settings]:
    """get the settings from .env file"""
    return Settings
