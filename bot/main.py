from telegram.ext import Application
from handlers.start import start_handler
from handlers.button import button_handler
from handlers.message import message_handler
import os

def main():
    TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
    application = Application.builder().token(TELEGRAM_TOKEN).build()
    application.add_handler(start_handler)
    application.add_handler(button_handler)
    application.add_handler(message_handler)
    application.run_polling()

if __name__ == "__main__":
    main()
