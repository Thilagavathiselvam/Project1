import json
import os

USER_FILE = "users.json"

# ---------- User Management ----------
def load_users():
    """Load existing users from JSON file."""
    if os.path.exists(USER_FILE):
        try:
            with open(USER_FILE, "r") as f:
                return json.load(f)
        except json.JSONDecodeError:
            return {}  # In case file is empty or broken
    return {}

def save_users(users):
    """Save users to JSON file."""
    with open(USER_FILE, "w") as f:
        json.dump(users, f, indent=4)

def signup_user(email, password):
    """Create a new user account."""
    users = load_users()
    if email in users:
        return False  # user already exists
    users[email] = {"password": password, "predictions": []}
    save_users(users)
    return True

def login_user(email, password):
    """Check login credentials."""
    users = load_users()
    if email in users and users[email]["password"] == password:
        return True
    return False


# ---------- Prediction Storage ----------
def save_prediction(email, prediction_data):
    """Save a prediction record for the user."""
    users = load_users()
    if email not in users:
        return False

    if "predictions" not in users[email]:
        users[email]["predictions"] = []

    users[email]["predictions"].append(prediction_data)
    save_users(users)
    return True

def load_predictions(email):
    """Load all predictions for the user."""
    users = load_users()
    if email in users and "predictions" in users[email]:
        return users[email]["predictions"]
    return []
