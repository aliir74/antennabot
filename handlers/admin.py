from typing import TYPE_CHECKING

from telegram import Update

from config import ADMIN_CHAT_IDS
from utils.logger import user_logger

if TYPE_CHECKING:
    from telegram.ext import ContextTypes


async def handle_report_command(
    update: Update, context: "ContextTypes.DEFAULT_TYPE"
) -> None:
    """Handle the /report command - admin only."""
    if not update.message or update.effective_user.id not in ADMIN_CHAT_IDS:
        return

    try:
        # Get statistics
        stats = user_logger.get_stats()

        if not stats:
            await update.message.reply_text("آماری موجود نیست.")
            return

        # Format statistics into a readable message
        report = "📊 گزارش آماری ربات:\n\n"

        # User statistics
        report += (
            f"👥 تعداد کل کاربران: {stats['total_users']}\n"
            f"👤 کاربران یکتا: {stats['unique_users']}\n\n"
        )

        # Action statistics
        actions = stats["actions"]
        report += "🔄 آمار عملیات:\n"
        report += f"▫️ دستور شروع: {actions['start_command']}\n"

        # File downloads
        downloads = actions["file_downloads"]
        report += "\n📥 دانلود فایل‌ها:\n"
        report += f"▫️ همراه اول: {downloads.get('mci', 0)}\n"
        report += f"▫️ ایرانسل: {downloads.get('irancell', 0)}\n"
        report += f"▫️ رایتل: {downloads.get('rightel', 0)}\n"

        # Other statistics
        report += f"\n📹 مشاهده آموزش: {actions['tutorial_views']}\n"
        report += f"🔍 بررسی عضویت: {actions['subscription_checks']}\n"

        # Last update time
        last_updated = stats["last_updated"].split("T")[0]  # Get just the date
        report += f"\n🕒 آخرین بروزرسانی: {last_updated}"

        await update.message.reply_text(report)

    except Exception as e:
        await update.message.reply_text(
            "متأسفانه در دریافت آمار خطایی رخ داد. لطفاً دوباره تلاش کنید."
        )
