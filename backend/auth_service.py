from backend import auth, session
from database import user_queries


def register_user(username, email, password):
    valid, message = auth.validate_username(username)
    if not valid:
        return None, message

    valid, message = auth.validate_password(password)
    if not valid:
        return None, message

    existing_user = user_queries.get_user_by_username(username)
    if existing_user is not None:
        return None, "Username already exists"

    password_hash = auth.hash_password(password)
    user = user_queries.create_user(
        username,
        email,
        password_hash,
    )
    session.current_user = user
    return user, None


def authenticate_user(username, password):
    user = user_queries.get_user_by_username(username)
    if user is None:
        return None, "User not found"

    if not auth.check_password(user["password_hash"], password):
        return None, "Incorrect password"

    session.current_user = user
    return user, None
