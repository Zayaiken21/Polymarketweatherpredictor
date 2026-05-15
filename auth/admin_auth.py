from storage.settings_store import save_display_name, delete_user_data

def verify_ceo_password(password: str, expected_password: str) -> bool:
    return bool(password and expected_password and password == expected_password)

def update_display_name(user_id, display_name):
    save_display_name(user_id, display_name)

def delete_user(user_id):
    delete_user_data(user_id)