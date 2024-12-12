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
from utils.logger import user_logger

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
    if not update.message or not update.message.text or not update.effective_user:
        return

    message = update.message.text.lower()

    if message not in APN_CONFIGS:
        await update.message.reply_text(INVALID_APN_MESSAGE)
        return

    # Log the APN request
    user_logger.log_action(
        user_id=update.effective_user.id,
        username=update.effective_user.username or update.effective_user.first_name,
        action="apn_request",
        details={"apn_type": message}
    )

    # Store the requested APN in user data for later use
    context.user_data["requested_apn"] = message

    # Check channel subscription
    is_subscribed = await check_channel_subscription(
        update.effective_user.id, context.bot
    )

    if not is_subscribed:
        # Log subscription request
        user_logger.log_action(
            user_id=update.effective_user.id,
            username=update.effective_user.username or update.effective_user.first_name,
            action="subscription_required"
        )
        await send_subscription_message(update)
        return

    await send_config_file(update, context, message)


async def send_config_file(
    update: Update, context: "ContextTypes.DEFAULT_TYPE", apn: str
) -> None:
    """Send configuration file to user."""
    if not update.effective_user:
        return

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

        # Log successful file send
        user_logger.log_action(
            user_id=update.effective_user.id,
            username=update.effective_user.username or update.effective_user.first_name,
            action="file_sent",
            details={"apn_type": apn}
        )

        # Send tutorial link if enabled
        if (
            ENABLE_TUTORIAL_LINKS
            and YOUTUBE_TUTORIAL_LINKS
            and YOUTUBE_TUTORIAL_LINKS[0]
        ):
            await message.reply_text(f"📹 آموزش: {YOUTUBE_TUTORIAL_LINKS[0]}")
            
            # Log tutorial link sent
            user_logger.log_action(
                user_id=update.effective_user.id,
                username=update.effective_user.username or update.effective_user.first_name,
                action="tutorial_sent",
                details={"apn_type": apn}
            )

    except Exception as e:
        logger.error(f"Error sending file: {e}")
        # Log error
        user_logger.log_action(
            user_id=update.effective_user.id,
            username=update.effective_user.username or update.effective_user.first_name,
            action="error",
            details={"error": str(e), "apn_type": apn}
        )
        await message.reply_text(
            "متأسفانه در ارسال فایل خطایی رخ داد. لطفاً دوباره تلاش کنید."
        )
