import os
import asyncio
from dotenv import load_dotenv
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from keep_alive import keep_alive

load_dotenv()

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH"))
BOT_TOKEN = os.getenv("BOT_TOKEN")
BOT_USERNAME = os.getenv("BOT_USERNAME")
CHANNEL_USERNAME = os.getenv("CHANNEL_USERNAME")
ADMIN_ID = int(os.getenv("ADMIN_ID"))

app = Client("menfessbot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

sent_users = set()
blacklist = set()
total_users = set()
user_message_map = {}

user_preferences = {}

@app.on_message(filters.command("start") & filters.private)
async def start_handler(client, message):
    user_id = message.from_user.id
    total_users.add(user_id)
    user_preferences[user_id] = {
        "anon": True,
        "allow_reply": False,
        "gender": "Tidak disebutkan",
        "hashtag": ""
    }

    await message.reply(
        "👋 Selamat datang di bot Menfess!\n\n"
        "Kamu bisa mengirim pesan anonim ke channel.\n\n"
        "Gunakan tombol di bawah ini untuk mengatur preferensi kamu:",
        reply_markup=InlineKeyboardMarkup([
            [
                InlineKeyboardButton("🔒 Anonim", callback_data="pref_anon"),
                InlineKeyboardButton("👁️ Tampilkan Username", callback_data="pref_nick")
            ],
            [
                InlineKeyboardButton("✅ Izinkan Balasan", callback_data="pref_reply_yes"),
                InlineKeyboardButton("🚫 Tolak Balasan", callback_data="pref_reply_no")
            ],
            [
                InlineKeyboardButton("🚺 Perempuan", callback_data="pref_gender_f"),
                InlineKeyboardButton("🚹 Laki-laki", callback_data="pref_gender_m")
            ],
            [
                InlineKeyboardButton("#️⃣ Tambah Hashtag", callback_data="add_hashtag")
            ]
        ])
    )

@app.on_message(filters.command("help") & filters.private)
async def help_handler(client, message):
    await message.reply(
        "📖 *Bantuan Bot Menfess*\n\n"
        "Kirim pesan ke bot ini untuk diteruskan ke channel secara anonim.\n\n"
        "🔧 *Fitur yang tersedia:*\n"
        "- Kirim sebagai anonim atau tampilkan username\n"
        "- Izinkan atau larang balasan pribadi\n"
        "- Tambahkan hashtag untuk pesanmu\n"
        "- Tandai gender kamu (opsional)\n\n"
        "Ketik /start untuk memulai pengaturan.",
        quote=True
    )

@app.on_message(filters.command("menu") & filters.private)
async def menu_handler(client, message):
    await start_handler(client, message)

@app.on_callback_query()
async def callback_handler(client, callback_query):
    user_id = callback_query.from_user.id
    data = callback_query.data

    if user_id not in user_preferences:
        user_preferences[user_id] = {"anon": True, "allow_reply": False, "gender": "Tidak disebutkan", "hashtag": ""}

    if data == "pref_anon":
        user_preferences[user_id]["anon"] = True
        await callback_query.answer("Kamu memilih anonim.", show_alert=True)
    elif data == "pref_nick":
        user_preferences[user_id]["anon"] = False
        await callback_query.answer("Kamu memilih menampilkan username.", show_alert=True)
    elif data == "pref_reply_yes":
        user_preferences[user_id]["allow_reply"] = True
        await callback_query.answer("Kamu mengizinkan orang lain membalasmu.", show_alert=True)
    elif data == "pref_reply_no":
        user_preferences[user_id]["allow_reply"] = False
        await callback_query.answer("Kamu tidak mengizinkan balasan pribadi.", show_alert=True)
    elif data == "pref_gender_f":
        user_preferences[user_id]["gender"] = "Perempuan"
        await callback_query.answer("Identitas diset sebagai Perempuan.", show_alert=True)
    elif data == "pref_gender_m":
        user_preferences[user_id]["gender"] = "Laki-laki"
        await callback_query.answer("Identitas diset sebagai Laki-laki.", show_alert=True)
    elif data == "add_hashtag":
        await callback_query.message.reply("Kirimkan hashtag yang ingin kamu gunakan (contoh: #curhat, #menfess)")

@app.on_message(filters.private & filters.text & ~filters.command("start"))
async def hashtag_receiver(client, message):
    user_id = message.from_user.id
    if user_id in user_preferences and user_preferences[user_id].get("hashtag") == "pending":
        user_preferences[user_id]["hashtag"] = message.text.strip()
        await message.reply(f"✅ Hashtag berhasil disimpan: {message.text.strip()}")
    elif message.text.startswith("#"):
        await menfess_handler(client, message)
    else:
        await menfess_handler(client, message)

@app.on_message(filters.private & (filters.text | filters.photo))
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
            reply_markup = InlineKeyboardMarkup([
                [InlineKeyboardButton("✉️ Kirim pesan ke pengirim", url=f"https://t.me/{message.from_user.username}")]
            ])

        full_caption = ""
        if message.photo:
            caption = message.caption or "(Tanpa keterangan)"
            full_caption = f"📸 Pesan dari {identity} ({gender}) {hashtag}:\n\n{caption}{additional_caption}"
            sent_msg = await app.send_photo(CHANNEL_USERNAME, photo=message.photo.file_id, caption=full_caption, reply_markup=reply_markup)
        else:
            full_caption = f"📩 Pesan dari {identity} ({gender}) {hashtag}:\n\n{message.text}{additional_caption}"
            sent_msg = await app.send_message(CHANNEL_USERNAME, text=full_caption, reply_markup=reply_markup)

        if sent_msg:
            user_message_map[sent_msg.id] = (user_id, pref["allow_reply"], message.from_user.username)

        await message.reply("✅ Pesan berhasil dikirim!")
        sent_users.add(user_id)
        await asyncio.sleep(60)
        sent_users.remove(user_id)

    except Exception as e:
        print(f"Error: {e}")
        await message.reply(f"❌ Gagal mengirim pesan: {e}")

if __name__ == "__main__":
    keep_alive()
    app.run()
