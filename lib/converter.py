from pyrogram.types import Message
from pyrogram import Client, filters

from aspose import words


@Client.on_message(filters.command("pdf2docx"))
async def pdf2docx_(client, message):
    msg = await message.reply("`Processing...`")
    replied = message.reply_to_message
    if replied.document:
         file = await client.download_media(replied, file_name=f"{message.from_user.id}_in.pdf")
         doc = words.Document(file)
         doc.save(f"{message.from_user.id}_out.docx")
         await msg.edit("Processed ⬇️")
         await client.send_document(document=f"{message.from_user.id}_out.docx", chat_id=message.from_user.id)
    else:
         await message.reply("Unsupported file!")

