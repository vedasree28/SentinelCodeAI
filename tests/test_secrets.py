from src.core.secrets import detect_secrets

def test_secret_detection():
    code = 'API_KEY = "AKIA1234567890ABCDEF"'
    result = detect_secrets(code)

    assert len(result) > 0