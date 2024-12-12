from typing import TYPE_CHECKING, Union

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update

from config import SUBSCRIPTION_MESSAGE, TELEGRAM_CHANNEL

if TYPE_CHECKING:
    from telegram import Message, Update
    from telegram.ext import ContextTypes


async def check_channel_subscription(user_id: int, bot) -> bool:
    """Check if user is subscribed to the required channel."""
    try:
        member = await bot.get_chat_member(chat_id=TELEGRAM_CHANNEL, user_id=user_id)
        return member.status in ["member", "administrator", "creator"]
    except Exception as e:
        return False


async def send_subscription_message(update: Union["Update", "Message"]) -> None:
    """Send message asking user to subscribe to channel."""
    keyboard = [
        [
            InlineKeyboardButton(
                "عضویت در کانال", url=f"https://t.me/{TELEGRAM_CHANNEL.lstrip('@')}"
            )
        ],
        [InlineKeyboardButton("عضو شدم ✅", callback_data="check_subscription")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Handle both Update and Message objects
    message = update.message if isinstance(update, Update) else update

    await message.reply_text(
        SUBSCRIPTION_MESSAGE.format(channel=TELEGRAM_CHANNEL), reply_markup=reply_markup
    )
