"""Telegram bot for the pharmacy archive using a webhook."""
from __future__ import annotations
import logging
import os
from fastapi import FastAPI, Request
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
logging.basicConfig(
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    level=logging.INFO,
)
logging.getLogger("httpx").setLevel(logging.WARNING)
logging.getLogger("httpcore").setLevel(logging.WARNING)
token = os.getenv("TELEGRAM_BOT_TOKEN")
if not token:
    raise RuntimeError("TELEGRAM_BOT_TOKEN is not set.")
application = Application.builder().token(token).build()
app = FastAPI()
def archive_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        [
            [InlineKeyboardButton(label, url=url)]
            for label, url in ARCHIVE_LINKS
        ]
    )
async def start(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:
    if update.message is None:
        return
    await update.message.reply_text(
        WELCOME_MESSAGE,
        reply_markup=archive_keyboard(),
    )
async def help_command(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:
    await start(update, context)
application.add_handler(CommandHandler("start", start))
application.add_handler(CommandHandler("help", help_command))
@app.on_event("startup")
async def startup() -> None:
    webhook_url = os.getenv("RENDER_EXTERNAL_URL")
    if not webhook_url:
        raise RuntimeError("RENDER_EXTERNAL_URL is not available.")
    await application.initialize()
    await application.start()
    await application.bot.set_webhook(
        url=f"{webhook_url}/telegram",
        allowed_updates=Update.ALL_TYPES,
    )
    logging.info("Pharmacy archive bot webhook is running.")
@app.on_event("shutdown")
async def shutdown() -> None:
    await application.stop()
    await application.shutdown()
@app.get("/")
async def home():
    return {"status": "Pharmacy archive bot is running"}
@app.post("/telegram")
async def telegram_webhook(request: Request):
    data = await request.json()
    update = Update.de_json(
        data=data,
        bot=application.bot,
    )
    await application.process_update(update)
    return {"ok": True}
