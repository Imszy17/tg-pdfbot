import os

from PIL import Image
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

from config import BOT_LOG
from database.list_user_db import add_user_list, rem_user_list
from database.ocr_db import add_user_ocr, list_ocr_user, rem_user_ocr
from database.pdf_db import add_user_pdf, list_pdf_user, rem_user_pdf

START_MSG = """Ini adalah bot yang dapat membantu pekerjaan yang berhubungan dengan file document.

**💡 Fitur:**
__1. Mengubah beberapa gambar menjadi file .pdf
2. Konversi file .pdf ke .docx tanpa menghilangkan spasi
3. Membaca text pada sebuah gambar dengan teknologi OCR__

⚠️ `Bot dalam masa pengembangan, mungkin dapat aktif dan nonaktif secara tiba-tiba dan tanpa pemberitahuan`

👨‍💻 **Pengembang:** @gmardiana
"""

LIST = {}


@Client.on_callback_query(filters.regex(pattern=r"mode_pdf"))
async def mode_pdf_cb(b, cb):
    id = cb.message.from_user.id
    try:
        rem_user_ocr(int(id))
    except:
        pass
    add_user_pdf(int(id))
    await cb.message.edit("Mode diubah ke pdf")


@Client.on_callback_query(filters.regex(pattern=r"mode_ocr"))
async def mode_ocr_cb(b, cb):
    id = cb.message.from_user.id
    try:
        rem_user_pdf(int(id))
    except:
        pass
    add_user_ocr(int(id))
    await cb.message.edit("Mode diubah ke ocr")


@Client.on_message(filters.photo)
async def start(client, message):
    keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("PDF", callback_data="mode_pdf"),
                InlineKeyboardButton("OCR", callback_data="mode_ocr"),
            ],
        ]
    )
    user_id = message.from_user.id
    pdf_user = list_pdf_user()
    ocr_user = list_ocr_user()
    if user_id in pdf_user:
        id = message.from_user.id
        if not isinstance(LIST.get(id), list):
            LIST[id] = []
        file_id = str(message.photo.file_id)
        text = await message.reply_text("```Processing...```")
        file = await client.download_media(file_id)
        image = Image.open(file)
        img = image.convert("RGB")
        LIST[id].append(img)
        await text.edit(
            f"{len(LIST[id])} Gambar berhasil ditambahkan, klik **/pdf** untuk membuat pdf, atau tambahkan gambar lainnya"
        )
    elif user_id in ocr_user:
        await message.reply("this is ocr")
    else:
        await message.reply(
            "Silahkan pilih perintah yang anda inginkan!", reply_markup=keyboard
        )


@Client.on_message(filters.command(["pdf"]))
async def convert(client, message):
    log_id = int(BOT_LOG)
    msg = await message.reply("Memproses...")
    id = message.from_user.id
    info = message.from_user.mention
    images = LIST.get(id)
    if isinstance(images, list):
        del LIST[id]
    if not images:
        await msg.edit("Tidak ada gambar!")
        return
    path = f"{id}" + ".pdf"
    images[0].save(path, save_all=True, append_images=images[1:])
    await client.send_document(id, open(path, "rb"), caption="Pdf sudah siap!")
    await client.send_message(log_id, f"{info}\n{id}\nStatus: Mengakses bot")
    await msg.delete()
    os.remove(path)
