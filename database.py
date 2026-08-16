import json
import os

DB_FILE = "security_db.json"

def load_db():
    if not os.path.exists(DB_FILE):
        with open(DB_FILE, "w") as f:
            json.dump({"approved_pms": [], "sudo_users": [], "locked_groups": []}, f)
    with open(DB_FILE, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return {"approved_pms": [], "sudo_users": [], "locked_groups": []}

def save_db(data):
    with open(DB_FILE, "w") as f:
        json.dump(data, f, indent=4)

def is_approved(user_id):
    db = load_db()
    return user_id in db.get("approved_pms", [])

def approve_user(user_id):
    db = load_db()
    if user_id not in db["approved_pms"]:
        db["approved_pms"].append(user_id)
        save_db(db)

def disallow_user(user_id):
    db = load_db()
    if user_id in db["approved_pms"]:
        db["approved_pms"].remove(user_id)
        save_db(db)

def is_sudo(user_id):
    db = load_db()
    return user_id in db.get("sudo_users", [])

def add_sudo(user_id):
    db = load_db()
    if user_id not in db["sudo_users"]:
        db["sudo_users"].append(user_id)
        save_db(db)

def rm_sudo(user_id):
    db = load_db()
    if user_id in db["sudo_users"]:
        db["sudo_users"].remove(user_id)
        save_db(db)

def is_group_locked(chat_id):
    db = load_db()
    return chat_id in db.get("locked_groups", [])

def lock_group(chat_id):
    db = load_db()
    if chat_id not in db["locked_groups"]:
        db["locked_groups"].append(chat_id)
        save_db(db)

def unlock_group(chat_id):
    db = load_db()
    if chat_id in db["locked_groups"]:
        db["locked_groups"].remove(chat_id)
        save_db(db)
