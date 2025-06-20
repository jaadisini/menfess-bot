from pyrogram import Client
from pyrogram.types import CallbackQuery
from data.state import user_message_map
from utils.logger import log_event

votes = {}

@Client.on_callback_query()
async def vote_cb(c,q:CallbackQuery):
    data=q.data
    if data.startswith("vote_"):
        mid=data.split("_")[1]
        votes[mid]=votes.get(mid,0)+1
        await q.answer(f"👍 Vote: {votes[mid]}")
        await log_event(c,f"👍 Vote by {q.from_user.id} for {mid}")

