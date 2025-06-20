# This file handles logging to LOG_CHAT_ID
from config import LOG_CHAT_ID

async def log_event(client, text):
    if LOG_CHAT_ID != 0:
        try:
            await client.send_message(LOG_CHAT_ID, text)
        except Exception as e:
            print(f"[LOGGING FAILED] {e}")
