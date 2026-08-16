import time
from telethon import events
from database import is_sudo

def setup(client):
    @client.on(events.NewMessage(pattern=r"(?i)^\.ping"))
    async def ping_command(event):
        if not (event.out or is_sudo(event.sender_id)):
            return
            
        start_time = time.time()
        if event.out:
            message = await event.edit("🏓 **Pong!**")
        else:
            message = await event.reply("🏓 **Pong!**")
        end_time = time.time()
        
        ping_time = round((end_time - start_time) * 1000)
        await message.edit(f"🏓 **Pong!**\n📶 Latency: `{ping_time}ms`")
