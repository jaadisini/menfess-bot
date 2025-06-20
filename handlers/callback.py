from pyrogram import Client
from pyrogram.types import CallbackQuery
from data.state import user_preferences

@Client.on_callback_query()
async def callback_handler(client, callback_query: CallbackQuery):
    user_id = callback_query.from_user.id
    data = callback_query.data

    if user_id not in user_preferences:
        user_preferences[user_id] = {"anon": True, "allow_reply": False, "gender": "Tidak disebutkan", "hashtag": ""}

    pref = user_preferences[user_id]

    if data == "pref_anon":
        pref["anon"] = True
        await callback_query.answer("Kamu memilih anonim.", show_alert=True)
    elif data == "pref_nick":
        pref["anon"] = False
        await callback_query.answer("Kamu memilih menampilkan username.", show_alert=True)
    elif data == "pref_reply_yes":
        pref["allow_reply"] = True
        await callback_query.answer("Kamu mengizinkan orang lain membalasmu.", show_alert=True)
    elif data == "pref_reply_no":
        pref["allow_reply"] = False
        await callback_query.answer("Kamu tidak mengizinkan balasan pribadi.", show_alert=True)
    elif data == "pref_gender_f":
        pref["gender"] = "Perempuan"
        await callback_query.answer("Identitas diset sebagai Perempuan.", show_alert=True)
    elif data == "pref_gender_m":
        pref["gender"] = "Laki-laki"
        await callback_query.answer("Identitas diset sebagai Laki-laki.", show_alert=True)
    elif data == "add_hashtag":
        pref["hashtag"] = "pending"
        await callback_query.message.reply("Kirimkan hashtag yang ingin kamu gunakan (contoh: #curhat, #menfess)")
