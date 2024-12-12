import os
from typing import Dict

from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Bot Configuration
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHANNEL = os.getenv("TELEGRAM_CHANNEL", "@My_Channel")
ENABLE_TUTORIAL_LINKS = os.getenv("ENABLE_TUTORIAL_LINKS", "true").lower() == "true"
YOUTUBE_TUTORIAL_LINKS = os.getenv("YOUTUBE_TUTORIAL_LINKS", "").split(",")
DONATE_LINK = os.getenv("DONATE_LINK", "")
# APN Configurations
APN_CONFIGS: Dict[str, Dict[str, str]] = {
    "mci": {
        "file_path": "files/mci_config.txt",
        "description": "MCI Configuration File",
    },
    "irancell": {
        "file_path": "files/irancell_config.txt",
        "description": "Irancell Configuration File",
    },
    "rightel": {
        "file_path": "files/rightel_config.txt",
        "description": "Rightel Configuration File",
    },
}

# Messages
WELCOME_MESSAGE = """سلام {first_name}! 👋

لطفاً نوع سیم‌کارت خود را برای دریافت فایل تنظیمات انتخاب کنید.
گزینه‌های موجود:
- همراه اول
- ایرانسل
- رایتل"""

SUBSCRIPTION_MESSAGE = """لطفاً ابتدا در کانال {channel} عضو شوید!
پس از عضویت، دکمه زیر را برای دریافت فایل کلیک کنید."""

INVALID_APN_MESSAGE = """متأسفانه این نوع سیم‌کارت شناسایی نشد. لطفاً از گزینه‌های زیر انتخاب کنید:
- همراه اول
- ایرانسل
- رایتل"""

NOT_SUBSCRIBED_MESSAGE = (
    "شما هنوز در کانال {channel} عضو نشده‌اید. لطفاً عضو شوید و دوباره تلاش کنید!"
)
SEND_APN_AGAIN_MESSAGE = "لطفاً نوع سیم‌کارت خود را دوباره ارسال کنید."
ERROR_SENDING_FILE = "متأسفانه در ارسال فایل خطایی رخ داد. لطفاً دوباره تلاش کنید."
