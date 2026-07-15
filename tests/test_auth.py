from backend import auth


def test_password_hash_is_salted_and_verifiable():
    first_hash = auth.hash_password("correct horse")
    second_hash = auth.hash_password("correct horse")

    assert first_hash != second_hash
    assert auth.check_password(first_hash, "correct horse")
    assert not auth.check_password(first_hash, "wrong password")


def test_password_hash_accepts_postgres_hex_format():
    password_hash = auth.hash_password("correct horse")
    database_value = "\\x" + password_hash.hex()

    assert auth.check_password(database_value, "correct horse")


def test_username_validation():
    assert auth.validate_username("Gio") == (True, "")
    assert auth.validate_username("")[0] is False
    assert auth.validate_username("Gio2")[0] is False
    assert auth.validate_username("Gio  Espinoza")[0] is False


def test_password_validation():
    assert auth.validate_password("eightchars")[0] is True
    assert auth.validate_password("short")[0] is False
    assert auth.validate_password("two  spaces")[0] is False
