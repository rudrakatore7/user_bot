from telethon import events
import random
from database import is_sudo

SLAPS = [
    "slapped {} with a large trout",
    "gave {} a high five... in the face",
    "threw a brick at {}",
    "hit {} with a frying pan",
    "dropkicked {}"
]

def setup(client):
    @client.on(events.NewMessage(pattern=r"(?i)^\.slap$"))
    async def slap_cmd(event):
        if not (event.out or is_sudo(event.sender_id)): return
        if not event.is_reply:
            return await event.edit("⚠️ **Reply to someone to slap them.**") if event.out else await event.reply("⚠️ **Reply to someone to slap them.**")
            
        reply = await event.get_reply_message()
        user = await reply.get_sender()
        name = user.first_name if user else "them"
        
        action = random.choice(SLAPS).format(f"**{name}**")
        await event.edit(f"🖐 {action}!") if event.out else await event.reply(f"🖐 {action}!")

    @client.on(events.NewMessage(pattern=r"(?i)^\.insult$"))
    async def insult_cmd(event):
        if not (event.out or is_sudo(event.sender_id)): return
        if not event.is_reply:
            return await event.edit("⚠️ **Reply to someone to insult them.**") if event.out else await event.reply("⚠️ **Reply to someone to insult them.**")
            
        insults = [
            "You're like a software update. Whenever I see you, I think 'Not now'.",
            "If laughter is the best medicine, your face must be curing the world.",
            "You are proof that God has a sense of humor."
        ]
        await event.edit(random.choice(insults)) if event.out else await event.reply(random.choice(insults))
