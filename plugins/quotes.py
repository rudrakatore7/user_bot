from telethon import events
import urllib.request
import json
from database import is_sudo

def setup(client):
    @client.on(events.NewMessage(pattern=r"(?i)^\.quote$"))
    async def quote_cmd(event):
        if not (event.out or is_sudo(event.sender_id)): return
        msg = await event.edit("💭 **Thinking...**") if event.out else await event.reply("💭 **Thinking...**")
        
        try:
            url = "https://api.quotable.io/random"
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            response = urllib.request.urlopen(req)
            data = json.loads(response.read().decode())
            
            content = data.get('content', 'No quote found.')
            author = data.get('author', 'Unknown')
            
            await msg.edit(f"❝ `{content}` ❞\n— **{author}**")
        except Exception:
            await msg.edit("❌ **Could not fetch a quote.**")
