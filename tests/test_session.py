import pytest

from backend import session


def test_current_user_id(monkeypatch):
    monkeypatch.setattr(session, "current_user", {"user_id": 42, "username": "Gio"})

    assert session.get_current_user_id() == 42


def test_current_user_id_requires_login(monkeypatch):
    monkeypatch.setattr(session, "current_user", None)

    with pytest.raises(ValueError, match="No user is currently logged in"):
        session.get_current_user_id()
