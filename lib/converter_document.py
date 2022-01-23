from pyrogram.types import Message
from pyrogram import Client, filters

from aspose import words


@Client.on_message(filters.command("pdf2docx"))
async def pdf2docx_(client, message):
    msg = await message.reply("`Memproses...`")
    replied = message.reply_to_message
    userID = message.from_user.id
    if replied.document:
         file = await client.download_media(replied, file_name=f"{userID}_in.pdf")
         doc = words.Document(file)
         doc.save(f"{userID}_out.docx")
         await msg.edit("Selesai ⬇️")
         await client.send_document(document=f"{userID}_out.docx", chat_id=userID)
    elif not replied.document:
         await message.reply("Balaskan perintah pada sebuah gambar!")
    else:
         await message.reply("Unsupported file!")

