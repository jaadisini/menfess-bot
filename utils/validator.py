import re

def is_valid_username(username: str) -> bool:
    """
    Validasi username Telegram dimulai dengan @ dan panjang 5-32 karakter.
    """
    return username.startswith("@") and 5 <= len(username) <= 32

def is_valid_menfess_content(text: str) -> bool:
    """
    Validasi isi menfess tidak kosong dan minimal 10 karakter bersih.
    """
    return bool(text and len(text.strip()) >= 10)

def is_valid_hashtag(text: str) -> bool:
    """
    Validasi hashtag format #contoh, tanpa spasi, panjang maksimal 32.
    """
    return bool(re.fullmatch(r"#\w{1,32}", text))
