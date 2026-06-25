current_user = None

def get_current_user_id():
    if current_user is None:
        raise ValueError("No user is currently logged in.")
    return current_user["user_id"]