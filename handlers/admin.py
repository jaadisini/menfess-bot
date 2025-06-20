from pyrogram import Client, filters
from pyrogram.types import Message
from data.state import user_preferences
from config import ADMIN_ID
from utils.logger import log_event

@Client.on_message(filters.private & filters.command("broadcast"))
async def bc(c,m:Message):
    if m.from_user.id!=ADMIN_ID:
        return await m.reply("🚫 Only admin")
    parts=m.text.split(None,1)
    if len(parts)<2: return await m.reply("Usage: /broadcast text")
    txt=parts[1]; s=f=0
    for u in user_preferences:
        try: await c.send_message(u,txt); s+=1
        except: f+=1
    await m.reply(f"✅ done. sent={s} fail={f}")
    await log_event(c,f"📢 Broadcast by admin: {s}/{f}")

