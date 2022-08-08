from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

from database.list_user_db import add_user_list, rem_user_list
from database.pdf_db import add_pdf_list, list_pdf_user

START_MSG = """Ini adalah bot yang dapat membantu pekerjaan yang berhubungan dengan file document.

**💡 Fitur:**
__1. Mengubah beberapa gambar menjadi file .pdf
2. Konversi file .pdf ke .docx tanpa menghilangkan spasi
3. Membaca text pada sebuah gambar dengan teknologi OCR__

⚠️ `Bot dalam masa pengembangan, mungkin dapat aktif dan nonaktif secara tiba-tiba dan tanpa pemberitahuan`

👨‍💻 **Pengembang:** @gmardiana
"""


@Client.on_callback_query(filters.regex(pattern=r"mode_pdf"))
async def mode_pdf_cb(b, cb):
    add_pdf_list()
    await cb.message.reply("Mode diubah ke pdf")


@Client.on_message(filters.command("start"))
async def start(client, message):
    keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("PDF", callback_data="mode_pdf"),
                InlineKeyboardButton("OCR", callback_data="cls"),
            ],
        ]
    )
    user_id = message.from_user.id
    pdf_user = list_pdf_user()
    if user_id not in pdf_user:
        await message.reply("Silahkan pilih mode!", reply_markup=keyboard)
    else:
        try:
            mention = message.from_user.mention
            id = message.from_user.id
            add_user_list(int(id))
            await message.reply(
                f"**Hai {mention}** 👋\n{START_MSG}", disable_web_page_preview=True
            )
        except Exception as e:
            await message.reply("Kesalahan sistem!\n" + e)
