from pyrogram import Client, filters
from pyrogram.types import Message

START_MSG = """Ini adalah bot yang dapat membantu pekerjaan yang berhubungan dengan file document.
**💡 Fitur:**

1. Mengubah beberapa gambar menjadi file .pdf
2. Konversi file .pdf ke .docx tanpa menghilangkan spasi
3. Membaca text pada sebuah gambar dengan teknologi OCR

⚠️ `Bot dalam masa pengembangan, mungkin dapat aktif dan nonaktif secara tiba-tiba

👨‍💻  Pengembang [GalihMrd](https://t.me/gmardiana)
"""

@Client.on_message(filters.command("start"))
async def start(client, message):
    id = message.from_user.mention
    await message.reply(f"**Hai {id}** 👋\n{START_MSG}", disable_web_page_preview=True)
