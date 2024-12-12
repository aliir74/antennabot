import logging
from typing import TYPE_CHECKING, Optional

from telegram import Message, Update

from config import (
    APN_CONFIGS,
    DONATE_LINK,
    ENABLE_TUTORIAL_LINKS,
    INVALID_APN_MESSAGE,
    YOUTUBE_TUTORIAL_LINKS,
)

from .subscription import check_channel_subscription, send_subscription_message

if TYPE_CHECKING:
    from telegram.ext import ContextTypes

logger = logging.getLogger(__name__)


def get_message_from_update(update: Update) -> Optional[Message]:
    """Extract message object from update safely."""
    if update.callback_query and update.callback_query.message:
        return update.callback_query.message
    elif update.message:
        return update.message
    return None


async def handle_apn_request(
    update: Update, context: "ContextTypes.DEFAULT_TYPE"
) -> None:
    """Handle user messages and process APN requests."""
    if not update.message or not update.message.text:
        return

    message = update.message.text.lower()

    if message not in APN_CONFIGS:
        await update.message.reply_text(INVALID_APN_MESSAGE)
        return

    # Store the requested APN in user data for later use
    context.user_data["requested_apn"] = message

    # Check channel subscription
    is_subscribed = await check_channel_subscription(
        update.effective_user.id, context.bot
    )

    if not is_subscribed:
        await send_subscription_message(update)
        return

    await send_config_file(update, context, message)


async def send_config_file(
    update: Update, context: "ContextTypes.DEFAULT_TYPE", apn: str
) -> None:
    """Send configuration file to user."""
    # Get the message object first
    message = get_message_from_update(update)
    if not message:
        logger.error("No message object found in update")
        return

    # Validate APN and get config
    config = APN_CONFIGS.get(apn)
    if not config:
        logger.error(f"Invalid APN type: {apn}")
        await message.reply_text("نوع سیم‌کارت نامعتبر است. لطفاً دوباره تلاش کنید.")
        return

    try:
        # Answer callback query if present
        if update.callback_query:
            await update.callback_query.answer()

        # Send the configuration file
        with open(config["file_path"], "rb") as file:
            sent_message = await message.reply_document(
                document=file,
                filename=f"{apn}_config.txt",
                caption=(
                    f"فایل تنظیمات {apn.upper()} آماده است!\n\n"
                    "🙏 اگر این ربات برای شما مفید بود، می‌توانید از طریق لینک زیر از ما حمایت کنید:\n"
                    f"{DONATE_LINK}"
                ),
            )

        # Send tutorial link if enabled
        if (
            ENABLE_TUTORIAL_LINKS
            and YOUTUBE_TUTORIAL_LINKS
            and YOUTUBE_TUTORIAL_LINKS[0]
        ):
            await message.reply_text(f"📹 آموزش: {YOUTUBE_TUTORIAL_LINKS[0]}")

    except Exception as e:
        logger.error(f"Error sending file: {e}")
        await message.reply_text(
            "متأسفانه در ارسال فایل خطایی رخ داد. لطفاً دوباره تلاش کنید."
        )
