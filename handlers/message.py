import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from config import BOT_USERNAME, CHANNEL_USERNAME
from data.state import user_preferences, blacklist, sent_users, total_users, user_message_map

@Client.on_message(filters.private & filters.text)
async def handle_text_message(client, message: Message):
    user_id = message.from_user.id

    if user_id in user_preferences and user_preferences[user_id].get("hashtag") == "pending":
        user_preferences[user_id]["hashtag"] = message.text.strip()
        await message.reply(f"✅ Hashtag berhasil disimpan: {message.text.strip()}")
        return

    await menfess_handler(client, message)

@Client.on_message(filters.private & filters.photo)
async def menfess_handler(client, message: Message):
    user_id = message.from_user.id
    total_users.add(user_id)

    if user_id in blacklist:
        await message.reply("⛔ Kamu tidak diizinkan mengirim pesan ke bot ini.")
        return

    if user_id in sent_users:
        await message.reply("⚠️ Kamu sudah mengirim pesan. Mohon tunggu sebelum mengirim lagi.")
        return

    if message.text and len(message.text) > 4096:
        await message.reply("❗ Pesan terlalu panjang untuk dikirim. Maksimal 4096 karakter.")
        return

    await message.reply("Pesan kamu sedang dikirim ke channel...")

    try:
        pref = user_preferences.get(user_id, {"anon": True, "allow_reply": False, "gender": "Tidak disebutkan", "hashtag": ""})
        username = f"@{message.from_user.username}" if message.from_user.username else "(Tanpa username)"
        identity = "Anonim" if pref["anon"] else username
        gender = pref.get("gender", "Tidak disebutkan")
        hashtag = pref.get("hashtag", "")

        additional_caption = f"\n\n📢 Pesan ini dikirim melalui @{BOT_USERNAME}"

        reply_markup = None
        if pref["allow_reply"] and not pref["anon"] and message.from_user.username:
            reply_markup = InlineKeyboardMarkup([[
                InlineKeyboardButton("✉️ Kirim pesan ke pengirim", url=f"https://t.me/{message.from_user.username}")
            ]])

        if message.photo:
            caption = message.caption or "(Tanpa keterangan)"
            full_caption = f"📸 Pesan dari {identity} ({gender}) {hashtag}:\n\n{caption}{additional_caption}"
            sent_msg = await client.send_photo(CHANNEL_USERNAME, message.photo.file_id, caption=full_caption, reply_markup=reply_markup)
        else:
            full_caption = f"📩 Pesan dari {identity} ({gender}) {hashtag}:\n\n{message.text}{additional_caption}"
            sent_msg = await client.send_message(CHANNEL_USERNAME, text=full_caption, reply_markup=reply_markup)

        if sent_msg:
            user_message_map[sent_msg.id] = (user_id, pref["allow_reply"], message.from_user.username)

        await message.reply("✅ Pesan berhasil dikirim!")
        sent_users.add(user_id)
        await asyncio.sleep(60)
        sent_users.remove(user_id)

    except Exception as e:
        await message.reply(f"❌ Gagal mengirim pesan: {e}")
        print(f"Error: {e}")
