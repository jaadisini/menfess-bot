import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from data.state import user_preferences, blacklist, pending_replies, user_message_map, stats
from config import BOT_USERNAME, CHANNEL_USERNAME
from utils.logger import log_event

@Client.on_message(filters.private & filters.text)
async def handle_text_message(client: Client, message: Message):
    uid = message.from_user.id

    # Handle pending replies
    if uid in pending_replies:
        await handle_pending_reply(client, message, uid)
        return

    # Handle hashtag saving
    if user_preferences[uid].get("hashtag") == "pending":
        await save_hashtag(message, uid)
        return

    # Check for blacklist
    if uid in blacklist:
        return await message.reply("⛔ You are blacklisted.")

    # Prepare to send the message to the channel
    await send_to_channel(client, message, uid)

async def handle_pending_reply(client: Client, message: Message, uid: int):
    target = int(pending_replies.pop(uid))
    original_data = user_message_map.get(str(target))
    
    if not original_data:
        return await message.reply("❌ Cannot find the original sender.")
    
    target_uid, allow_reply, username = original_data
    if not allow_reply:
        return await message.reply("🚫 The original sender doesn't allow replies.")
    
    try:
        await client.send_message(target_uid, f"💬 Reply for your menfess:\n\n{message.text}")
        await message.reply("✅ Reply sent.")
    except Exception as e:
        await message.reply("⚠️ Failed to send reply.")
        print(f"Error sending reply: {e}")
    
    await log_event(client, f"➰ Reply from {uid} to {target_uid}")

async def save_hashtag(message: Message, uid: int):
    user_preferences[uid]["hashtag"] = message.text.strip()
    await message.reply(f"✅ Hashtag saved: {message.text}")

async def send_to_channel(client: Client, message: Message, uid: int):
    pref = user_preferences.get(uid, {})
    hashtag = pref.get("hashtag", "")
    pref["hashtag"] = ""

    await message.reply("⏳ Sending to channel...")
    
    identity = "Anonim" if pref.get("anon", True) else f"@{message.from_user.username}"
    gender = pref.get("gender", "?")
    caption = f"{hashtag}\n📤 from {identity} ({gender})"
    
    buttons = [InlineKeyboardButton("💬 Reply", callback_data=f"reply_{message.message_id}")]
    if pref.get("allow_reply") and not pref.get("anon"):
        buttons.append(InlineKeyboardButton("✉️ DM Sender", url=f"https://t.me/{message.from_user.username}"))
    
    keyboard = InlineKeyboardMarkup([buttons])

    sent_message = None
    try:
        if message.photo:
            sent_message = await client.send_photo(CHANNEL_USERNAME, message.photo.file_id, caption=caption, reply_markup=keyboard)
        else:
            sent_message = await client.send_message(CHANNEL_USERNAME, caption, reply_markup=keyboard)

        if sent_message:
            user_message_map[str(sent_message.message_id)] = [uid, pref.get("allow_reply", False), message.from_user.username]
            stats["total_menfess"] += 1
            if hashtag:
                stats["popular_hashtags"][hashtag] = stats["popular_hashtags"].get(hashtag, 0) + 1

        await message.reply("✅ Sent.")
        await log_event(client, f"📤 Menfess {sent_message.message_id} by {uid}")
    except Exception as e:
        await message.reply("⚠️ Failed to send to channel.")
        print(f"Error sending to channel: {e}")

    await asyncio.sleep(60)
