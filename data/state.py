from data.storage import load_json, save_json

user_preferences = load_json("users.json", {})
blacklist = set(load_json("blacklist.json", []))
user_message_map = load_json("messages.json", {})
stats = load_json("stats.json", {
    "total_users": 0,
    "total_menfess": 0,
    "popular_hashtags": {}
})

def save_all():
    save_json("users.json", user_preferences)
    save_json("blacklist.json", list(blacklist))
    save_json("messages.json", user_message_map)
    save_json("stats.json", stats)
    
pending_replies = {}