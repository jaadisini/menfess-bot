from pyrogram import Client, filters
from pyrogram.types import Message
from data.state import stats, user_preferences
from config import ADMIN_ID

@Client.on_message(filters.private & filters.command("stats"))
async def st(c,m:Message):
    if m.from_user.id!=ADMIN_ID:
        return await m.reply("🚫 Admin only")
    total=len(user_preferences)
    tm=stats["total_menfess"]
    ph=stats["popular_hashtags"]
    top=sorted(ph.items(), key=lambda x:x[1], reverse=True)[:3]
    taglist="\n".join(f"{k}:{v}" for k,v in top) or "—"
    await m.reply(f"📊 Users:{total}\nMenfess:{tm}\nHashtags:\n{taglist}")

