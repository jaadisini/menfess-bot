from utils.validator import is_valid_username, is_valid_menfess_content, is_valid_hashtag

def test_valid_usernames():
    assert is_valid_username("@aesneverhere") is True
    assert is_valid_username("@abcde") is True

def test_invalid_usernames():
    assert is_valid_username("aesneverhere") is False
    assert is_valid_username("@a") is False

def test_menfess_content_valid():
    assert is_valid_menfess_content("Aku mau confess ke dia") is True

def test_menfess_content_invalid():
    assert is_valid_menfess_content("  ") is False
    assert is_valid_menfess_content("Hi") is False

def test_valid_hashtag():
    assert is_valid_hashtag("#rindu") is True
    assert is_valid_hashtag("#halo123") is True

def test_invalid_hashtag():
    assert is_valid_hashtag("rindu") is False
    assert is_valid_hashtag("#") is False
    assert is_valid_hashtag("#ini_hashtag_yang_panjang_bangettttttttttttttt") is False
