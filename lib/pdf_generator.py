import os
from PIL import Image
from config import BOT_LOG
from pyrogram import Client, filters


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
             img = image.convert('RGB')
             LIST[id].append(img)
             await text.edit(f"{len(LIST[id])} Gambar berhasil ditambahkan, klik **/pdf** untuk membuat pdf, atau tambahkan gambar lainnya")
    except BaseException:
        await message.reply("Balaskan perintah pada gambar yang akan dikonversi ke .pdf !")


@Client.on_message(filters.command(['pdf']))
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
    images[0].save(path, save_all = True, append_images = images[1:])
    await client.send_document(id, open(path, "rb"), caption = "Pdf sudah siap!")
    await client.send_message(log_id, f"{info}\n{id}\nStatus: Mengakses bot")
    await msg.delete()
    os.remove(path)
