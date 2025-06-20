from pyrogram import Client
from pyrogram.types import CallbackQuery
from data.state import user_preferences, pending_replies
from utils.logger import log_event

@Client.on_callback_query()
async def cb(c, q:CallbackQuery):
    uid, data = q.from_user.id, q.data
    user_preferences.setdefault(uid,{})

    pref = user_preferences[uid]
    if data=="pref_anon": pref["anon"]=True
    elif data=="pref_nick": pref["anon"]=False
    elif data=="pref_reply_yes": pref["allow_reply"]=True
    elif data=="pref_reply_no": pref["allow_reply"]=False
    elif data=="pref_gender_f": pref["gender"]="Perempuan"
    elif data=="pref_gender_m": pref["gender"]="Laki-laki"
    elif data=="add_hashtag":
        pref["hashtag"]="pending"; await q.message.reply("Send hashtag (e.g. #curhat)")
        await q.answer(); return
    await q.answer(f"Set {data}")
    await log_event(c,f"⚙️ Pref updated by {uid}: {data}")