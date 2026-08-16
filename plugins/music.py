from telethon import events
import urllib.request
import json
from database import is_sudo

def setup(client):
    @client.on(events.NewMessage(pattern=r"(?i)^\.lyrics (.*)"))
    async def lyrics_cmd(event):
        if not (event.out or is_sudo(event.sender_id)): return
        song_name = event.pattern_match.group(1).replace(" ", "%20")
        msg = await event.edit("🔍 **Searching for lyrics...**") if event.out else await event.reply("🔍 **Searching for lyrics...**")
        
        try:
            url = f"https://some-random-api.com/lyrics?title={song_name}"
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            response = urllib.request.urlopen(req)
            data = json.loads(response.read().decode())
            
            title = data.get('title', 'Unknown')
            author = data.get('author', 'Unknown')
            lyrics = data.get('lyrics', 'No lyrics found.')
            
            # Telegram message limit is 4096 chars
            if len(lyrics) > 3800:
                lyrics = lyrics[:3800] + "...\n(Truncated due to length)"
                
            out = f"🎵 **{title}** by **{author}**\n\n`{lyrics}`"
            await msg.edit(out)
        except Exception:
            await msg.edit("❌ **Could not find lyrics for that song.**")
