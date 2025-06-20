from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from data.state import user_preferences, total_users

@Client.on_message(filters.command("start") & filters.private)
async def start_handler(client, message: Message):
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

@Client.on_message(filters.command(["help", "menu"]) & filters.private)
async def help_handler(client, message: Message):
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
