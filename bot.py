import os
from telegram.ext import Updater, MessageHandler, Filters
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
TOKEN = os.getenv("BOT_TOKEN")

SYSTEM_PROMPT = (
    "You are a warm, romantic, flirty AI companion. "
    "Keep replies suggestive but non-explicit. "
    "Be caring, playful, and respectful. Hindi allowed."
)

def reply(update, context):
    user_text = update.message.text

    resp = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_text},
        ],
        max_tokens=120,
        temperature=0.8
    )

    update.message.reply_text(resp.choices[0].message.content)

updater = Updater(TOKEN, use_context=True)
updater.dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, reply))
updater.start_polling()
updater.idle()
