import os
from dotenv import load_dotenv
import ollama
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters

load_dotenv()
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

SYSTEM_PROMPT = """
You are an AI assistant that only provides information about animals. 
If a user asks about anything unrelated to animals, politely refuse to answer.
"""

async def start(update: Update, context):
    await update.message.reply_text("Hello! Ask me anything about Animals.")

async def handle_message(update: Update, context):
    user_message = update.message.text
    print(f"User: {user_message}")

    response = ollama.chat(
        model="gemma:2b",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_message}
        ]
    )

    bot_reply = response['message']['content']

    print(f"Bot: {bot_reply}")
    await update.message.reply_text(bot_reply)

app = Application.builder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

print("GoodBot is running...")
app.run_polling()
