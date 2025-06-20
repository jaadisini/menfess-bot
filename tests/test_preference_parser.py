from utils.preference_parser import parse_preference

def test_parse_preference_basic():
    text = "gender=F umur=21 domisili=Bandung"
    expected = {"gender": "F", "umur": "21", "domisili": "Bandung"}
    assert parse_preference(text) == expected

def test_parse_preference_with_spaces():
    text = "  gender=F   umur=19    domisili=Jogja  "
    expected = {"gender": "F", "umur": "19", "domisili": "Jogja"}
    assert parse_preference(text) == expected

def test_parse_preference_empty():
    assert parse_preference("") == {}
