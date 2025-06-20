from pyrogram import Client
from config import API_ID, API_HASH, BOT_TOKEN
from keep_alive import keep_alive

# Import semua handler agar terdaftar
import handlers.start
import handlers.callback
import handlers.message

app = Client("menfessbot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

if __name__ == "__main__":
    keep_alive()
    app.run()
