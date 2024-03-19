import os
import random

from fpdf import FPDF
from PIL import Image
from pyrogram import filters
from pyromod import Client, Message

from config import BOT_LOG

LIST = {}


@Client.on_message(filters.command("addpic"))
async def pdf(client, message):
    replied = message.reply_to_message
    try:
        if replied.photo:
            id = message.from_user.id
            if not isinstance(LIST.get(id), list):
                LIST[id] = []
            file_id = str(replied.photo.file_id)
            text = await message.reply_text("`Memproses...`")
            file = await client.download_media(file_id)
            image = Image.open(file)
            img = image.convert("RGB")
            LIST[id].append(img)
            await text.edit(
                f"{len(LIST[id])} Gambar berhasil ditambahkan, klik **/pdf** untuk membuat pdf, atau tambahkan gambar lainnya"
            )
    except BaseException:
        await message.reply(
            "Balaskan perintah pada gambar yang akan dikonversi ke .pdf !"
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


@Client.on_message(filters.command("text2pdf"))
async def txt2pdf(client: Client, message: Message):
    log_id = int(BOT_LOG)
    chat = message.chat
    to_pdf = await chat.ask(
        "Silahkan kirim text yang akan dijadikan pdf.", filters=filters.text
    )
    f = open("to_pdf.txt", "w")
    f.write(to_pdf.text)
    f.close()
    names = random.randint(1000, 10000)
    print(to_pdf)
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=11)
    f = open("to_pdf.txt", "r")
    pdf_name = f"{names}_{message.from_user.id}.pdf"
    for x in f:
        pdf.cell(150, 10, txt=x, ln=1, align="L")
    pdf.output(pdf_name)
    await client.send_document(
        message.from_user.id, pdf_name, caption="Pdf sudah siap!"
    )
    await client.send_message(
        log_id, f"{message.from_user.mention}\nStatus: Mengakses bot"
    )
    os.remove(pdf_name)
