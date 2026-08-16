from telethon import events
import base64
import asyncio
from database import is_sudo

def setup(client):
    @client.on(events.NewMessage(pattern=r"(?i)^\.b64(en|de) (.*)"))
    async def b64_cmd(event):
        if not (event.out or is_sudo(event.sender_id)): return
        action = event.pattern_match.group(1).lower()
        text = event.pattern_match.group(2)
        try:
            if action == "en":
                res = base64.b64encode(text.encode("utf-8")).decode("utf-8")
                msg = f"🔐 **Encoded:**\n`{res}`"
            else:
                res = base64.b64decode(text.encode("utf-8")).decode("utf-8")
                msg = f"🔓 **Decoded:**\n`{res}`"
            await event.edit(msg) if event.out else await event.reply(msg)
        except Exception as e:
            err = f"⚠️ **Error:** `{e}`"
            await event.edit(err) if event.out else await event.reply(err)
            
    @client.on(events.NewMessage(pattern=r"(?i)^\.timer (\d+)"))
    async def timer_cmd(event):
        if not (event.out or is_sudo(event.sender_id)): return
        seconds = int(event.pattern_match.group(1))
        msg = await event.edit(f"⏳ **Timer started for {seconds} seconds!**") if event.out else await event.reply(f"⏳ **Timer started for {seconds} seconds!**")
        await asyncio.sleep(seconds)
        await msg.reply(f"⏰ **BEEP BEEP! Your {seconds}s timer is done!**")
