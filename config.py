import os
from typing import Dict, List

from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Bot Configuration
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHANNEL = os.getenv("TELEGRAM_CHANNEL", "@My_Channel")
ENABLE_TUTORIAL_LINKS = os.getenv("ENABLE_TUTORIAL_LINKS", "true").lower() == "true"
YOUTUBE_TUTORIAL_LINKS = os.getenv("YOUTUBE_TUTORIAL_LINKS", "").split(",")
DONATE_LINK = os.getenv("DONATE_LINK", "")
DATA_DIR = os.getenv("DATA_DIR", "/app/data")
# Admin Configuration
ADMIN_CHAT_IDS: List[int] = [
    int(id_)
    for id_ in os.getenv("ADMIN_CHAT_IDS", "").split(",")
    if id_.strip().isdigit()
]

# APN Configurations
APN_CONFIGS: Dict[str, Dict[str, str]] = {
    "mci": {
        "file_path": "files/base.mobileconfig",
        "description": "MCI Configuration File",
    },
    "irancell": {
        "file_path": "files/base.mobileconfig",
        "description": "Irancell Configuration File",
    },
    "rightel": {
        "file_path": "files/base.mobileconfig",
        "description": "Rightel Configuration File",
    },
    "shatel": {
        "file_path": "files/base.mobileconfig",
        "description": "Shatel Configuration File",
    },
    "samantel": {
        "file_path": "files/base.mobileconfig",
        "description": "Samantel Configuration File",
    },
}

# Messages
WELCOME_MESSAGE = """سلام {first_name}! 👋

لطفاً نوع سیم‌کارت خود را برای دریافت فایل تنظیمات انتخاب کنید.
گزینه‌های موجود:
- همراه اول
- ایرانسل
- رایتل
- شاتل
- سامانتل"""

SUBSCRIPTION_MESSAGE = """لطفاً ابتدا در کانال {channel} عضو شوید!
پس از عضویت، دکمه زیر را برای دریافت فایل کلیک کنید."""

INVALID_APN_MESSAGE = """متأسفانه این نوع سیم‌کارت شناسایی نشد. لطفاً از گزینه‌های زیر انتخاب کنید:
- همراه اول
- ایرانسل
- رایتل
- شاتل
- سامانتل"""

NOT_SUBSCRIBED_MESSAGE = (
    "شما هنوز در کانال {channel} عضو نشده‌اید. لطفاً ع��و شوید و دوباره تلاش کنید!"
)
SEND_APN_AGAIN_MESSAGE = "لطفاً نوع سیم‌کارت خود را دوباره ارسال کنید."
ERROR_SENDING_FILE = "متأسفانه در ارسال فایل خطایی رخ داد. لطفاً دوباره تلاش کنید."
