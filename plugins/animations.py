from telethon import events
import asyncio
from database import is_sudo

def setup(client):
    @client.on(events.NewMessage(pattern=r"(?i)^\.hack$"))
    async def hack_cmd(event):
        if not (event.out or is_sudo(event.sender_id)): return
        msg = await event.edit("💻 **Initializing Hack...**") if event.out else await event.reply("💻 **Initializing Hack...**")
        anim = [
            "Accessing NSA Servers...",
            "Bypassing Firewalls... [██░░░░░░░░] 20%",
            "Bypassing Firewalls... [█████░░░░░] 50%",
            "Bypassing Firewalls... [█████████░] 90%",
            "Access Granted. Downloading Data...",
            "Decrypting Passwords...",
            "Data Stolen Successfully! 😈"
        ]
        for a in anim:
            await asyncio.sleep(1)
            await msg.edit(f"💻 **{a}**")
            
    @client.on(events.NewMessage(pattern=r"(?i)^\.magic$"))
    async def magic_cmd(event):
        if not (event.out or is_sudo(event.sender_id)): return
        msg = await event.edit("✨") if event.out else await event.reply("✨")
        anim = ["⚡", "🌪", "☄️", "💥", "🔥", "🔮 **MAGIC COMPLETE** 🔮"]
        for a in anim:
            await asyncio.sleep(0.5)
            await msg.edit(a)
