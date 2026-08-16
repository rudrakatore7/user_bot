from telethon import events
from telethon.tl.functions.contacts import BlockRequest
from database import is_approved, approve_user, disallow_user, is_sudo

WARNING_MSG = (
    "🛑 **Security System Active** 🛑\n\n"
    "I am currently away. Please state your business and wait for me to approve your PM.\n"
    "⚠️ *Spamming will result in an automatic block.*"
)

spam_counter = {}

def setup(client):
    @client.on(events.NewMessage(incoming=True, func=lambda e: e.is_private))
    async def pm_guard(event):
        user = await event.get_sender()
        if user.bot or user.is_self or user.verified:
            return
            
        chat_id = event.chat_id
        if is_approved(chat_id) or is_sudo(chat_id):
            return
            
        count = spam_counter.get(chat_id, 0)
        count += 1
        spam_counter[chat_id] = count
        
        if count == 1:
            await event.reply(WARNING_MSG)
        elif count >= 4:
            await event.reply("🚫 **You have been blocked for spamming.**")
            await client(BlockRequest(id=chat_id))
            
    @client.on(events.NewMessage(outgoing=True, pattern=r"(?i)^\.approve$"))
    async def approve_cmd(event):
        if event.is_private:
            chat_id = event.chat_id
        elif event.is_reply:
            reply = await event.get_reply_message()
            chat_id = reply.sender_id
        else:
            await event.edit("⚠️ Reply to a user or use this in their PM to approve them.")
            return
            
        approve_user(chat_id)
        if chat_id in spam_counter:
            del spam_counter[chat_id]
        await event.edit("✅ **User approved for PMs.**")

    @client.on(events.NewMessage(outgoing=True, pattern=r"(?i)^\.disallow$"))
    async def disallow_cmd(event):
        if event.is_private:
            chat_id = event.chat_id
        elif event.is_reply:
            reply = await event.get_reply_message()
            chat_id = reply.sender_id
        else:
            await event.edit("⚠️ Reply to a user or use this in their PM to disallow them.")
            return
            
        disallow_user(chat_id)
        await event.edit("❌ **User disallowed from PMs.**")
