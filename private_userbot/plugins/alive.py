import time
from telethon import events
from database import is_sudo

# Keep track of when the bot started
BOT_START_TIME = time.time()

def get_uptime():
    uptime_sec = round(time.time() - BOT_START_TIME)
    mins, sec = divmod(uptime_sec, 60)
    hours, mins = divmod(mins, 60)
    days, hours = divmod(hours, 24)
    
    if days > 0:
        return f"{days}d {hours}h {mins}m {sec}s"
    return f"{hours}h {mins}m {sec}s"

def setup(client):
    @client.on(events.NewMessage(pattern=r"(?i)^\.alive"))
    async def alive_command(event):
        if not (event.out or is_sudo(event.sender_id)):
            return
            
        uptime = get_uptime()
        alive_msg = (
            "🤖 **Private Userbot is Online!**\n\n"
            f"⏱ **Uptime:** `{uptime}`\n"
            "⚙️ **Status:** `Maximum Security Active`\n"
            "🛡 **Engine:** `Telethon Fortress`"
        )
        if event.out:
            await event.edit(alive_msg)
        else:
            await event.reply(alive_msg)
