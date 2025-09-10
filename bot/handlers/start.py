from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CommandHandler, ContextTypes
from utils.api import HUGGING_MODELS

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton(model["name"], callback_data=f"model_{model['id']}")] for model in HUGGING_MODELS
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "👋 Hello! Choose an AI model to start chatting:", reply_markup=reply_markup
    )
    context.user_data["chosen_model"] = HUGGING_MODELS[0]["id"]

start_handler = CommandHandler("start", start)
