def parse_preference(text: str) -> dict:
    """
    Mengubah teks preferensi seperti 'gender=F umur=20' jadi dict.
    """
    result = {}
    for part in text.strip().split():
        if '=' in part:
            key, value = part.split('=', 1)
            result[key.lower()] = value.strip()
    return result
