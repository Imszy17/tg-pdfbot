from pyrogram import Client, filters
from pyrogram.types import Message

START_MSG = """Saya adalah bot yang dapat mengubah gambar menjadi pdf, kamu tinggal kirim beberapa gambar lalu ketik /pdf

Saya diciptakan oleh [GalihMrd](https://t.me/gmardiana)
"""

@Client.on_message(filters.command("start"))
async def start(client, message):
    id = message.from_user.mention
    await message.reply(f"**Hai {id}** 👋\n{START_MSG}")
