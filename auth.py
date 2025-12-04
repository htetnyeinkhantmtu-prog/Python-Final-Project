import bcrypt
import time
import uuid
from storage import load_users, save_users


def username_valid(username):
    if len(username) < 5:
        return False, "Username must be at least 5 characters long."
    allowed_chars = "abcdefghijklmnopqrstuvwxyz0123456789_"
    if not all(c in allowed_chars for c in username):
        return False, "Username can only contain lowercase letters, numbers and _'."
    return True, ""


def password_strength(password):
    if len(password) < 8:
        return False, "Password must be at least 8 characters."
    if not any(c.isupper() for c in password):
        return False, "Must include uppercase letter."
    if not any(c.islower() for c in password):
        return False, "Must include lowercase letter."
    if not any(c.isdigit() for c in password):
        return False, "Must include a number."
    if not any(c in "!@#$%^&*()-_=+[]{};:,.<>?/\\|" for c in password):
        return False, "Must include a special character."
    return True, ""


def find_user(username, data):
    """Case-sensitive search for a username."""
    return next((u for u in data["users"] if u["username"] == username), None)


def register(username, password):
    valid, msg = username_valid(username)
    if not valid:
        return False, msg

    data = load_users()

    if find_user(username, data):
        return False, "Username already taken."

    strong, msg = password_strength(password)
    if not strong:
        return False, msg

    password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    user_id = str(uuid.uuid4())

    data["users"].append({
        "id": user_id,
        "username": username,
        "password_hash": password_hash,
        "failed_attempts": 0,
        "lock_until": None,
        "answers": [],
        "profile_complete": False
    })

    save_users(data)
    return True, "Registration successful!"


def login(username, password):
    data = load_users()
    user = find_user(username, data)

    if not user:
        return False, "Login Failed.", None

    if user.get("lock_until") and time.time() < user["lock_until"]:
        remaining = int(user["lock_until"] - time.time())
        mins = remaining // 60
        secs = remaining % 60
        return False, f"Account locked. Try again in {mins}m {secs}s.", None

    if bcrypt.checkpw(password.encode(), user["password_hash"].encode()):
        user["failed_attempts"] = 0
        user["lock_until"] = None
        save_users(data)
        return True, "Login successful!", username

    user["failed_attempts"] = user.get("failed_attempts", 0) + 1
    if user["failed_attempts"] >= 3:
        user["lock_until"] = time.time() + 3 * 60

    save_users(data)
    return False, "Login Failed.", None
