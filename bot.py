import logging

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CallbackQueryHandler, CommandHandler, ContextTypes

from config import TELEGRAM_BOT_TOKEN, WELCOME_MESSAGE
from handlers import handle_button_callback
from handlers.admin import handle_report_command
from utils.logger import user_logger

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    if not update.message or not update.effective_user:
        return

    user = update.effective_user

    # Log the start command
    user_logger.log_action(
        user_id=user.id,
        username=user.username or user.first_name,
        action="start_command",
    )

    keyboard = [
        [InlineKeyboardButton("همراه اول", callback_data="apn_mci")],
        [InlineKeyboardButton("ایرانسل", callback_data="apn_irancell")],
        [InlineKeyboardButton("رایتل", callback_data="apn_rightel")],
        [InlineKeyboardButton("شاتل", callback_data="apn_shatel")],
        [InlineKeyboardButton("سامانتل", callback_data="apn_samantel")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        WELCOME_MESSAGE.format(first_name=user.first_name), reply_markup=reply_markup
    )


async def wrapped_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Wrapper for callback query handler to include logging."""
    if not update.callback_query or not update.effective_user:
        return

    # Log the callback action
    user_logger.log_action(
        user_id=update.effective_user.id,
        username=update.effective_user.username or update.effective_user.first_name,
        action="button_click",
        details={"callback_data": update.callback_query.data},
    )

    # Handle the callback
    await handle_button_callback(update, context)


def main() -> None:
    """Start the bot."""
    # Create the Application
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("report", handle_report_command))
    application.add_handler(CallbackQueryHandler(wrapped_callback))

    # Start the Bot
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
