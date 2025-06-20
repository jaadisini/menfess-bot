from pyrogram import Client, filters
from pyrogram.types import Message
from config import BOT_USERNAME

@Client.on_message(filters.regex(r"^#\w+") & filters.private)
async def hashsrch(c,m:Message):
    tag=m.text.strip()
    await m.reply(f"Search: https://t.me/{BOT_USERNAME}?q={tag}")
