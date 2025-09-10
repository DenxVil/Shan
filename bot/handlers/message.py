from telegram.ext import MessageHandler, filters, ContextTypes
from utils.api import get_ai_response, HUGGING_MODELS
from utils.style import stylize_text

async def handle_message(update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    model_id = context.user_data.get("chosen_model", HUGGING_MODELS[0]["id"])
    response = await get_ai_response(user_text, model_id)
    reply_text = stylize_text(response)
    await update.message.reply_text(reply_text, parse_mode='HTML')

message_handler = MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message)