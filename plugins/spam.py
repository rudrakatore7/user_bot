from telethon import events
import asyncio
from database import is_sudo

def setup(client):
    @client.on(events.NewMessage(pattern=r"(?i)^\.spam (\d+) (.*)"))
    async def spam_cmd(event):
        if not (event.out or is_sudo(event.sender_id)): return
        count = int(event.pattern_match.group(1))
        text = event.pattern_match.group(2)
        
        # Hard limit to prevent abuse
        if count > 50:
            count = 50
            
        if event.out: await event.delete()
        
        for _ in range(count):
            await client.send_message(event.chat_id, text)
            await asyncio.sleep(0.5) # Prevent flood waits

    @client.on(events.NewMessage(pattern=r"(?i)^\.dspam (\d+) (\d+) (.*)"))
    async def dspam_cmd(event):
        if not (event.out or is_sudo(event.sender_id)): return
        delay = float(event.pattern_match.group(1))
        count = int(event.pattern_match.group(2))
        text = event.pattern_match.group(3)
        
        if count > 50:
            count = 50
            
        if event.out: await event.delete()
        
        for _ in range(count):
            await client.send_message(event.chat_id, text)
            await asyncio.sleep(delay)
