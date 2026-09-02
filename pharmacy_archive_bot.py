"""Telegram bot for the pharmacy archive."""
from __future__ import annotations
import logging
import os
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, ContextTypes

ARCHIVE_LINKS = (
    ("📚 أرشيف سنة أولى", "https://t.me/pharmacy_y1"),
    ("📚 أرشيف سنة ثانية", "https://t.me/+tQKpJIwFVZg3Zjdk"),
    ("📚 أرشيف سنة ثالثة", "https://t.me/+HEsSgP2CXfNkNGY0"),
    ("📚 أرشيف سنة رابعة وخامسة", "https://t.me/+c39qNJt2MYEzMTk8"),
)

WELCOME_MESSAGE = (
    "مرحباً بك في أرشيف كلية الصيدلة 📚\n\n"
    "اختر السنة الدراسية للوصول إلى الأرشيف:"
)

def archive_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        [
            [InlineKeyboardButton(label, url=url)]
            for label, url in ARCHIVE_LINKS
        ]
    )

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.message is None:
        return
    await update.message.reply_text(
        WELCOME_MESSAGE,
        reply_markup=archive_keyboard(),
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await start(update, context)

def main() -> None:
    token = os.getenv("TELEGRAM_BOT_TOKEN")

    if not token:
        raise RuntimeError(
            "TELEGRAM_BOT_TOKEN is not set."
        )

    logging.basicConfig(
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        level=logging.INFO,
    )

    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("httpcore").setLevel(logging.WARNING)

    application = Application.builder().token(token).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))

    logging.info("Pharmacy archive bot is running.")

    application.run_polling(
        allowed_updates=Update.ALL_TYPES
    )

if __name__ == "__main__":
    main()
