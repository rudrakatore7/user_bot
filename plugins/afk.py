from telethon import events
import time

IS_AFK = False
AFK_REASON = ""
AFK_TIME = 0

def setup(client):
    global IS_AFK, AFK_REASON, AFK_TIME
    
    @client.on(events.NewMessage(outgoing=True, pattern=r"(?i)^\.afk(?: |$)(.*)"))
    async def afk_cmd(event):
        global IS_AFK, AFK_REASON, AFK_TIME
        IS_AFK = True
        AFK_REASON = event.pattern_match.group(1).strip()
        AFK_TIME = time.time()
        msg = "😴 **I am now AFK.**"
        if AFK_REASON:
            msg += f"\n📝 **Reason:** `{AFK_REASON}`"
        await event.edit(msg)

    @client.on(events.NewMessage(outgoing=True))
    async def un_afk(event):
        global IS_AFK
        if IS_AFK and not event.text.startswith(".afk"):
            IS_AFK = False
            await event.reply("⏰ **I am back online! (AFK Mode disabled)**")
            
    @client.on(events.NewMessage(incoming=True, func=lambda e: e.is_private or e.mentioned))
    async def afk_reply(event):
        global IS_AFK, AFK_REASON
        if IS_AFK:
            msg = "😴 **I am currently AFK.**"
            if AFK_REASON:
                msg += f"\n📝 **Reason:** `{AFK_REASON}`"
            await event.reply(msg)
