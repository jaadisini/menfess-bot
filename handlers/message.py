import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from data.state import user_preferences, blacklist, pending_replies, user_message_map, stats
from config import BOT_USERNAME, CHANNEL_USERNAME
from utils.logger import log_event

@Client.on_message(filters.private & filters.text)
async def txt(c,m:Message):
    uid=m.from_user.id
    if uid in pending_replies:
        target=int(pending_replies.pop(uid))
        od=user_message_map.get(str(target))
        if not od: return await m.reply("❌ cannot find original sender")
        tuid, allow, uname = od
        if not allow: return await m.reply("🚫 original doesn't allow reply")
        try:
            await c.send_message(tuid, f"💬 Reply for your menfess:\n\n{m.text}")
            await m.reply("✅ reply sent")
        except:
            await m.reply("⚠️ failed sending reply")
        await log_event(c,f"➰ Reply from {uid} to {tuid}")
        return

    if user_preferences[uid].get("hashtag")=="pending":
        user_preferences[uid]["hashtag"]=m.text.strip()
        return await m.reply(f"✅ hashtag saved: {m.text}")

    if uid in blacklist: return await m.reply("⛔ blacklisted")
    pref=user_preferences.get(uid,{}); hs=pref.get("hashtag","")
    pref["hashtag"]=""

    await m.reply("⏳ sending to channel...")
    identity = "Anonim" if pref.get("anon",True) else f"@{m.from_user.username}"
    gender=pref.get("gender", "?")
    caption=f"{hs}\n📤 from {identity} ({gender})"
    btns=[InlineKeyboardButton("💬 Reply", callback_data=f"reply_{m.message_id}")]
    if pref.get("allow_reply") and not pref.get("anon"):
        btns.append(InlineKeyboardButton("✉️ DM Sender", url=f"https://t.me/{m.from_user.username}"))
    keyboard=InlineKeyboardMarkup([btns])

    sent=None
    if m.photo:
        sent=await c.send_photo(CHANNEL_USERNAME, m.photo.file_id, caption=caption, reply_markup=keyboard)
    else:
        sent=await c.send_message(CHANNEL_USERNAME, caption, reply_markup=keyboard)

    if sent:
        user_message_map[str(sent.message_id)] = [uid, pref.get("allow_reply", False), m.from_user.username]
        stats["total_menfess"]+=1
        if hs: stats["popular_hashtags"][hs]=stats["popular_hashtags"].get(hs,0)+1

    await m.reply("✅ sent.")
    await log_event(c,f"📤 Menfess {sent.message_id} by {uid}")
    await asyncio.sleep(60)