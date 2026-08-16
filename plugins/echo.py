from telethon import events
from database import is_sudo

ECHO_USERS = set()

def setup(client):
    @client.on(events.NewMessage(pattern=r"(?i)^\.addecho$"))
    async def addecho_cmd(event):
        if not (event.out or is_sudo(event.sender_id)): return
        if not event.is_reply:
            msg = "⚠️ **Reply to a user to echo them.**"
            return await event.edit(msg) if event.out else await event.reply(msg)
            
        reply = await event.get_reply_message()
        ECHO_USERS.add(reply.sender_id)
        msg = "🔊 **Echo Activated! I will now repeat everything they say.**"
        await event.edit(msg) if event.out else await event.reply(msg)

    @client.on(events.NewMessage(pattern=r"(?i)^\.rmecho$"))
    async def rmecho_cmd(event):
        if not (event.out or is_sudo(event.sender_id)): return
        if not event.is_reply:
            msg = "⚠️ **Reply to a user to stop echoing them.**"
            return await event.edit(msg) if event.out else await event.reply(msg)
            
        reply = await event.get_reply_message()
        if reply.sender_id in ECHO_USERS:
            ECHO_USERS.remove(reply.sender_id)
        msg = "🔇 **Echo Deactivated.**"
        await event.edit(msg) if event.out else await event.reply(msg)
        
    @client.on(events.NewMessage(incoming=True))
    async def echo_runner(event):
        if event.sender_id in ECHO_USERS:
            await event.reply(event.text)
