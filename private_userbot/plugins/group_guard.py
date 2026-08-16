import re
from telethon import events
from database import is_group_locked, lock_group, unlock_group

def setup(client):
    @client.on(events.NewMessage(outgoing=True, pattern=r"(?i)^\.lockdown$"))
    async def lockdown_cmd(event):
        if event.is_private:
            await event.edit("⚠️ This command is for groups only.")
            return
        
        lock_group(event.chat_id)
        await event.edit("🛡 **Group Lockdown Active!**\nLinks sent by regular members will be instantly deleted.")

    @client.on(events.NewMessage(outgoing=True, pattern=r"(?i)^\.unlock$"))
    async def unlock_cmd(event):
        if event.is_private:
            return
            
        unlock_group(event.chat_id)
        await event.edit("🔓 **Group Unlocked.**")
        
    @client.on(events.NewMessage(incoming=True))
    async def anti_spam(event):
        if event.is_private or event.out:
            return
            
        if not is_group_locked(event.chat_id):
            return
            
        # Check if message contains a link
        if re.search(r"(https?://|www\.)[^\s]+", event.raw_text, re.IGNORECASE):
            try:
                # Check if user is admin
                permissions = await client.get_permissions(event.chat_id, event.sender_id)
                if not permissions.is_admin and not permissions.is_creator:
                    await event.delete()
            except Exception:
                # Might fail if bot lacks admin rights in the group to get permissions or delete
                pass
