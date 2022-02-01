import os

import pytesseract
import requests
from PIL import Image
from pyrogram import Client, filters
from pyrogram.errors import MessageEmpty
from pyrogram.types import Message


@Client.on_message(filters.command("ocr"))
async def ocr(client, message):
    try:
        lang_code = message.command[1]
    except BaseException:
        lang_code = "eng"
    db_url = (
        f"https://github.com/galihmrd/tessdata/raw/main/{lang_code}.traineddata"
    )
    replied = message.reply_to_message
    dirs = r"./vendor/data/tessdata"
    path = os.path.join(dirs, f"{lang_code}.traineddata")
    if not os.path.exists(path):
        data = requests.get(
            db_url, allow_redirects=True, headers={"User-Agent": "Mozilla/5.0"}
        )
        if data.status_code == 200:
            open(path, "wb").write(data.content)
        else:
            return await message.reply(
                "`Kode bahasa salah, atau tidak didukung!`", parse_mode="md"
            )
    try:
        if replied.photo or replied.document:
            msg = await message.reply("`Memproses gambar...`")
            image = await client.download_media(
                replied, file_name=f"text_{message.from_user.id}.jpg"
            )
            img = Image.open(image)
            text = pytesseract.image_to_string(img, lang=f"{lang_code}")
            try:
                await msg.edit(text[:-1])
                os.remove(image)
            except MessageEmpty:
                return await message.reply("Teks tidak dapat diproses")
        else:
            await message.reply("input not found")
    except Exception as e:
        await msg.edit(f"**Kesalahan:** {e}")
