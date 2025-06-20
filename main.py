import atexit
from config import API_ID,API_HASH,BOT_TOKEN
from keep_alive import keep_alive
from data.state import save_all
import handlers.start, handlers.callback, handlers.message, handlers.admin, handlers.stats, handlers.hashtag_search, handlers.voting, handlers.moderasi
from pyrogram import Client

app=Client("menfess",api_id=API_ID,api_hash=API_HASH,bot_token=BOT_TOKEN)
atexit.register(save_all)

if __name__=="__main__":
    keep_alive(); app.run()

