from telethon import events
from database import is_sudo

def setup(client):
    @client.on(events.NewMessage(pattern=r"(?i)^\.shrug$"))
    async def shrug_cmd(event):
        if not (event.out or is_sudo(event.sender_id)): return
        msg = r"¯\_(ツ)_/¯"
        await event.edit(msg) if event.out else await event.reply(msg)

    @client.on(events.NewMessage(pattern=r"(?i)^\.lenny$"))
    async def lenny_cmd(event):
        if not (event.out or is_sudo(event.sender_id)): return
        msg = "( ͡° ͜ʖ ͡°)"
        await event.edit(msg) if event.out else await event.reply(msg)
        
    @client.on(events.NewMessage(pattern=r"(?i)^\.tableflip$"))
    async def tableflip_cmd(event):
        if not (event.out or is_sudo(event.sender_id)): return
        msg = "(╯°□°）╯︵ ┻━┻"
        await event.edit(msg) if event.out else await event.reply(msg)
