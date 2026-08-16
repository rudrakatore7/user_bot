import os
import sys
import glob
import importlib
from telethon import TelegramClient
from telethon.sessions import StringSession
from dotenv import load_dotenv

load_dotenv()
API_ID = os.getenv("API_ID")
API_HASH = os.getenv("API_HASH")
SESSION_NAME = os.getenv("SESSION_NAME", "my_userbot")
STRING_SESSION = os.getenv("STRING_SESSION", "")

if not API_ID or not API_HASH:
    sys.exit("[ERROR] API_ID or API_HASH is missing in your .env file!")

if STRING_SESSION:
    print("[*] Authenticating using StringSession from .env...")
    client = TelegramClient(StringSession(STRING_SESSION), int(API_ID), API_HASH)
else:
    print("[*] Authenticating using SQLite Session file...")
    client = TelegramClient(SESSION_NAME, int(API_ID), API_HASH)

def load_plugins():
    if not os.path.exists("plugins"):
        os.makedirs("plugins")
        with open(os.path.join("plugins", "__init__.py"), "w") as f:
            pass
            
    plugin_files = glob.glob("plugins/*.py")
    loaded_count = 0
    if os.getcwd() not in sys.path:
        sys.path.insert(0, os.getcwd())
        
    for file_path in plugin_files:
        module_name = os.path.basename(file_path)[:-3]
        if module_name == "__init__":
            continue
        try:
            module = importlib.import_module(f"plugins.{module_name}")
            if hasattr(module, 'setup'):
                module.setup(client)
            print(f"[*] Loaded plugin: {module_name}")
            loaded_count += 1
        except Exception as e:
            print(f"[ERROR] Failed to load {module_name}: {e}")
            
    return loaded_count

def start_bot():
    print("[*] Starting Private Userbot...")
    try:
        client.start(phone=lambda: sys.exit("\n[ERROR] CRITICAL: Session missing or broken!"))
    except Exception as e:
        sys.exit(f"\n[ERROR] Connection failed: {e}")
        
    print("[*] Successfully connected to Telegram!")
    count = load_plugins()
    print(f"[*] Successfully loaded {count} plugins.")
    print("[*] Bot is now running. Send .ping in any chat to test!")
    client.run_until_disconnected()

if __name__ == "__main__":
    start_bot()
