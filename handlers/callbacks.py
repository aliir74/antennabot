from typing import TYPE_CHECKING

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update

from config import NOT_SUBSCRIBED_MESSAGE, TELEGRAM_CHANNEL, APN_CONFIGS

from .apn import send_config_file, get_message_from_update
from .subscription import check_channel_subscription, send_subscription_message

if TYPE_CHECKING:
    from telegram.ext import ContextTypes


async def handle_button_callback(
    update: Update, context: "ContextTypes.DEFAULT_TYPE"
) -> None:
    """Handle button callbacks."""
    query = update.callback_query
    if not query or not query.message:
        return
        
    await query.answer()

    if query.data.startswith("apn_"):
        # Extract the APN type from callback data
        requested_apn = query.data.replace("apn_", "")
        
        # Validate APN type
        if requested_apn not in APN_CONFIGS:
            await query.message.reply_text("نوع سیم‌کارت نامعتبر است. لطفاً دوباره تلاش کنید.")
            return

        # Store the requested APN in user data
        context.user_data["requested_apn"] = requested_apn

        # Check channel subscription
        is_subscribed = await check_channel_subscription(
            query.from_user.id, context.bot
        )

        if not is_subscribed:
            await send_subscription_message(query.message)
            return

        await send_config_file(update, context, requested_apn)

    elif query.data == "check_subscription":
        is_subscribed = await check_channel_subscription(
            query.from_user.id, context.bot
        )

        if is_subscribed:
            requested_apn = context.user_data.get("requested_apn")
            if requested_apn:
                await send_config_file(update, context, requested_apn)
            else:
                # Send APN selection keyboard again
                keyboard = [
                    [InlineKeyboardButton("همراه اول", callback_data="apn_mci")],
                    [InlineKeyboardButton("ایرانسل", callback_data="apn_irancell")],
                    [InlineKeyboardButton("رایتل", callback_data="apn_rightel")],
                ]
                reply_markup = InlineKeyboardMarkup(keyboard)
                await query.message.reply_text(
                    "لطفاً نوع سیم‌کارت خود را انتخاب کنید:", reply_markup=reply_markup
                )
        else:
            await query.message.reply_text(
                NOT_SUBSCRIBED_MESSAGE.format(channel=TELEGRAM_CHANNEL)
            )
