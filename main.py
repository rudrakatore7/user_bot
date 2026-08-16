import os
import sys
import glob
import importlib
from telethon import TelegramClient
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
API_ID = os.getenv("API_ID")
API_HASH = os.getenv("API_HASH")
SESSION_NAME = os.getenv("SESSION_NAME", "my_userbot")

if not API_ID or not API_HASH:
    print("[ERROR] API_ID or API_HASH is missing in your .env file!")
    print("Please open the .env file, add your credentials, and try again.")
    sys.exit(1)

# Initialize the Telegram Client
client = TelegramClient(SESSION_NAME, int(API_ID), API_HASH)

def load_plugins():
    if not os.path.exists("plugins"):
        os.makedirs("plugins")
        # Create an __init__.py so Python treats it as a package
        with open(os.path.join("plugins", "__init__.py"), "w") as f:
            pass
            
    plugin_files = glob.glob("plugins/*.py")
    loaded_count = 0
    
    # Ensure the current directory is in the Python path so we can import 'plugins.X'
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
    
    # We pass a dummy phone function. If Telethon tries to ask for a phone number,
    # it means the session file is missing or broken. We crash instantly to tell the user.
    try:
        client.start(phone=lambda: sys.exit("\n[ERROR] CRITICAL: The server cannot find your session file! It is either missing, named incorrectly, or corrupted."))
    except Exception as e:
        print(f"\n[ERROR] Connection failed: {e}")
        sys.exit(1)
        
    print("[*] Successfully connected to Telegram!")
    
    # Load all plugins after client context is available
    count = load_plugins()
    print(f"[*] Successfully loaded {count} plugins.")
    print("[*] Bot is now running. Send .ping in any chat to test!")
    
    # Keep the bot running
    client.run_until_disconnected()

if __name__ == "__main__":
    start_bot()
