from config import LOG_CHAT_ID

async def log_event(client, text):
    if LOG_CHAT_ID != 0:
        try: await client.send_message(LOG_CHAT_ID, text)
        except Exception as e: print(f"[LOG FAILED] {e}")
