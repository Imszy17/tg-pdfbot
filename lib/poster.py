from pyrogram import Client, filters
from pyrogram.types import Message



template = f"""
**{tmp[0]}**
**Build Type:** {tmp[1]}
**Maintainer:** {tmp[2]}

**Changelogs:**
{tmp[3]}

**Notes:**
{tmp[4]}

**Credits & Thanks:**
{tmp[4]}

{tmp[5]}
"""


@Client.on_message(filters.command("post"))
async def poster(client, message):
    input = " ".join(message.command[1:])
    try:
        tmp = input.split("|")
        msg = await message.reply(template)
    except Exception as e:
        await msg.edit(e)
