from telethon import events
from database import is_sudo

def setup(client):
    @client.on(events.NewMessage(pattern=r"(?i)^\.ban$"))
    async def ban_cmd(event):
        if not (event.out or is_sudo(event.sender_id)): return
        if event.is_private: return await event.edit("⚠️ Only for groups.")
        if not event.is_reply: return await event.edit("⚠️ Reply to a user to ban.")
        reply = await event.get_reply_message()
        await client.edit_permissions(event.chat_id, reply.sender_id, view_messages=False)
        await event.edit("🔨 **User has been banned!**")

    @client.on(events.NewMessage(pattern=r"(?i)^\.kick$"))
    async def kick_cmd(event):
        if not (event.out or is_sudo(event.sender_id)): return
        if event.is_private: return await event.edit("⚠️ Only for groups.")
        if not event.is_reply: return await event.edit("⚠️ Reply to a user to kick.")
        reply = await event.get_reply_message()
        await client.kick_participant(event.chat_id, reply.sender_id)
        await event.edit("🥾 **User has been kicked!**")
        
    @client.on(events.NewMessage(pattern=r"(?i)^\.mute$"))
    async def mute_cmd(event):
        if not (event.out or is_sudo(event.sender_id)): return
        if event.is_private: return await event.edit("⚠️ Only for groups.")
        if not event.is_reply: return await event.edit("⚠️ Reply to a user to mute.")
        reply = await event.get_reply_message()
        await client.edit_permissions(event.chat_id, reply.sender_id, send_messages=False)
        await event.edit("🤐 **User has been muted!**")
