import re
from pyrogram import Client, filters
from pyrogram.types import Message

BADWORDS = ["spamword1","badword2"]
pattern = re.compile("|".join(map(re.escape,BADWORDS)), re.I)

@Client.on_message(filters.private & filters.text)
async def mod(c,m:Message):
    if pattern.search(m.text):
        return await m.reply("🚫 Detected forbidden words.")

