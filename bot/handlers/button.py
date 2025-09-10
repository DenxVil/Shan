from telegram.ext import CallbackQueryHandler, ContextTypes

async def button(update, context):
    query = update.callback_query
    await query.answer()
    data = query.data
    if data.startswith("model_"):
        chosen_model = data.split("_", 1)[1]
        context.user_data["chosen_model"] = chosen_model
        await query.edit_message_text(text=f"✅ Model selected: {chosen_model}\nType your message to get a reply!")

button_handler = CallbackQueryHandler(button)
