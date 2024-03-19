from pyrogram import Client, filters
from pyrogram.types import Message


START_MSG = """Ini adalah bot yang dapat membantu pekerjaan yang berhubungan dengan file document.

**💡 Fitur:**
__1. Mengubah beberapa gambar menjadi file .pdf
2. Konversi file .pdf ke .docx tanpa menghilangkan spasi
3. Membaca text pada sebuah gambar dengan teknologi OCR__

⚠️ `Bot dalam masa pengembangan, mungkin dapat aktif dan nonaktif secara tiba-tiba dan tanpa pemberitahuan`

👨‍💻 **Pengembang:** @gmardiana
"""


@Client.on_message(filters.command("start"))
async def start(client, message):
    try:
        mention = message.from_user.mention
        id = message.from_user.id
        await message.reply(
            f"**Hai {mention}** 👋\n{START_MSG}", disable_web_page_preview=True
        )
    except Exception as e:
        await message.reply("Kesalahan sistem!\n" + e)
