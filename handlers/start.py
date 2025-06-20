from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from data.state import user_preferences, stats
from utils.logger import log_event

@Client.on_message(filters.command(["start","help","menu"]) & filters.private)
async def start_handler(c, m:Message):
    uid=m.from_user.id
    if m.command[0]=="/start":
        user_preferences.setdefault(uid,{
            "anon":True,"allow_reply":False,
            "gender":"Tidak disebutkan","hashtag":""
        })
        stats["total_users"]=len(user_preferences)

    kb=[
      [InlineKeyboardButton("🔒 Anonim","pref_anon"),InlineKeyboardButton("👁️ Username","pref_nick")],
      [InlineKeyboardButton("✅ Allow Reply","pref_reply_yes"),InlineKeyboardButton("🚫 Deny Reply","pref_reply_no")],
      [InlineKeyboardButton("🚺 P","pref_gender_f"),InlineKeyboardButton("🚹 L","pref_gender_m")],
      [InlineKeyboardButton("#️⃣ Add Hashtag","add_hashtag")]
    ]
    await m.reply(
      "*Bot Menfess*\nUse menu buttons below.",
      reply_markup=InlineKeyboardMarkup(kb)
    )
    await log_event(c,f"✨ /{m.command[0][1:]} by {uid}")

