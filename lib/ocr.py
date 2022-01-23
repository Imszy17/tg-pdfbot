import os
import requests
import pytesseract
from PIL import Image
from pyrogram.types import Message
from pyrogram import Client, filters
from pyrogram.errors import MessageEmpty


@Client.on_message(filters.command("ocr"))
async def ocr(client, message):
    lang_code = message.command[1]
    db_url = f"https://github.com/tesseract-ocr/tessdata/raw/main/{lang_code}.traineddata"
    replied = message.reply_to_message
    dirs = r"./vendor/data/tessdata"
    path = os.path.join(dirs, f"{lang_code}.traineddata")
    if not os.path.exists(path):
         data = requests.get(db_url, allow_redirects=True, headers={'User-Agent': 'Mozilla/5.0'})
         if data.status_code == 200:
              open(path, 'wb').write(data.content)
         else:
              return await message.reply("`Either the lang code is wrong or the lang is not supported.`", parse_mode='md')
    if replied.photo:
         msg = await message.reply("`Processing images...`")
         image = await client.download_media(replied, file_name=f"text_{message.from_user.id}.jpg")
         img = Image.open(image)
         text = pytesseract.image_to_string(img, lang=f"{lang_code}")
         try:
             await msg.delete()
             await message.reply(text[:-1], quote=True, disable_web_page_preview=True)
         except MessageEmpty:
             return await message.reply("Text is not recognizable")
    else:
         await message.reply("input not found")
