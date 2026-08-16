from telethon import events

def setup(client):
    @client.on(events.NewMessage(outgoing=True, pattern=r"(?i)^\.purge$"))
    async def purge_command(event):
        # Check if the user replied to a message
        reply_msg = await event.get_reply_message()
        if not reply_msg:
            await event.edit("⚠️ **Error:** Reply to a message to start purging from there.")
            return
            
        # Optional: Show a quick animation
        await event.edit("🗑 **Purging messages...**")
        
        try:
            messages_to_delete = []
            # We want to delete every message starting from the replied message up to the command itself
            # We use iter_messages with min_id
            async for msg in client.iter_messages(event.chat_id, min_id=reply_msg.id - 1):
                messages_to_delete.append(msg.id)
                # Telegram has a limit of 100 messages per delete request
                if len(messages_to_delete) >= 100:
                    await client.delete_messages(event.chat_id, messages_to_delete)
                    messages_to_delete.clear()
                    
            # Delete any remaining messages
            if messages_to_delete:
                await client.delete_messages(event.chat_id, messages_to_delete)
                
            # Note: The .purge command itself is included in the deletion so it will disappear cleanly!
            
        except Exception as e:
            await event.edit(f"❌ **Failed to purge:** `{str(e)}`")
