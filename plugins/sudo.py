from telethon import events
from database import add_sudo, rm_sudo

def setup(client):
    @client.on(events.NewMessage(outgoing=True, pattern=r"(?i)^\.addsudo$"))
    async def addsudo_cmd(event):
        if not event.is_reply:
            await event.edit("⚠️ **Error:** Reply to a user's message to grant them Sudo access.")
            return
            
        reply = await event.get_reply_message()
        add_sudo(reply.sender_id)
        await event.edit("👑 **User granted Sudo access!**\nThey can now use your bot commands.")

    @client.on(events.NewMessage(outgoing=True, pattern=r"(?i)^\.rmsudo$"))
    async def rmsudo_cmd(event):
        if not event.is_reply:
            await event.edit("⚠️ **Error:** Reply to a user to revoke their Sudo access.")
            return
            
        reply = await event.get_reply_message()
        rm_sudo(reply.sender_id)
        await event.edit("🚫 **Sudo access revoked.**")
