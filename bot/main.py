import os
import logging
import requests
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackQueryHandler, ContextTypes

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
HUGGING_FACE_API_KEY = os.getenv("HF_API_KEY")
PERPLEXITY_API_KEY = os.getenv("PERPLEXITY_API_KEY")

HUGGING_MODELS = [
    {"name": "GPT-2", "id": "gpt2"},
    {"name": "DistilGPT2", "id": "distilgpt2"},
    {"name": "BLOOM", "id": "bigscience/bloom"},
]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton(model["name"], callback_data=f"model_{model['id']}")] for model in HUGGING_MODELS
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "👋 Hello! Choose an AI model to start chatting:", reply_markup=reply_markup
    )
    context.user_data["chosen_model"] = HUGGING_MODELS[0]["id"]

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data
    if data.startswith("model_"):
        chosen_model = data.split("_", 1)[1]
        context.user_data["chosen_model"] = chosen_model
        await query.edit_message_text(text=f"✅ Model selected: {chosen_model}\nType your message to get a reply!")

def stylize_text(text):
    return f"<b><code>{{text}}</code></b>"

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    model_id = context.user_data.get("chosen_model", HUGGING_MODELS[0]["id"])

    response = await get_ai_response(user_text, model_id)
    reply_text = stylize_text(response)
    await update.message.reply_text(reply_text, parse_mode='HTML')

async def get_ai_response(prompt, model_id):
    response = await hugging_face_request(prompt, model_id)
    if response:
        return response

    response = perplexity_request(prompt)
    if response:
        return response

    return "Sorry, no AI is available right now!"

def hugging_face_request(prompt, model_id):
    url = f"https://api-inference.huggingface.co/models/{{model_id}}"
    headers = {"Authorization": f"Bearer {{HUGGING_FACE_API_KEY}}"}
    data = {"inputs": prompt}
    try:
        resp = requests.post(url, headers=headers, json=data, timeout=8)
        if resp.status_code == 200:
            result = resp.json()
            if isinstance(result, list) and "generated_text" in result[0]:
                return result[0]["generated_text"]
            elif "generated_text" in result:
                return result["generated_text"]
            elif isinstance(result, str):
                return result
        return None
    except Exception:
        return None

def perplexity_request(prompt):
    url = "https://api.perplexity.ai/chat/completions"
    headers = {"Authorization": f"Bearer {{PERPLEXITY_API_KEY}}"}
    data = {"model": "pplx-7b-online", "messages": [{"role": "user", "content": prompt}]}
    try:
        resp = requests.post(url, headers=headers, json=data, timeout=8)
        if resp.status_code == 200:
            result = resp.json()
            return result.get("choices", [{}])[0].get("message", {}).get("content", None)
        return None
    except Exception:
        return None

def main():
    application = Application.builder().token(TELEGRAM_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    application.run_polling()

if __name__ == "__main__":
    main()