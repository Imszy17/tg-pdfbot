from pyrogram.types import Message
from pyrogram import Client, filters

from aspose import words


@Client.on_message(filters.command("pdf2docx"))
async def pdf2docx_(client, message):
    msg = await message.reply("`Memproses...`")
    replied = message.reply_to_message
    userID = message.from_user.id
    try:
        if replied.document:
             file = await client.download_media(replied, file_name=f"{userID}_in.pdf")
             doc = words.Document(file)
             doc.save(f"{userID}_out.docx")
             await msg.edit("Selesai ⬇️")
             await client.send_document(document=f"{userID}_out.docx", chat_id=userID)
        else:
             await message.reply("Unsupported file!")
    except BaseException:
        await msg.delete()
        await message.reply("Balaskan perintah pada sebuah dokumen.pdf !")


@Client.on_message(filters.command("text2docx"))
async def text2docx_(client, message):
    try:
        input = " ".join(message.command[1:])
        msg = await message.reply("Memproses...")
    except BaseException:
        await msg.edit("Input tidak kosong!")
    # Blank document
    doc = words.Document()
    # Write a document
    try:
        builder = words.DocumentBuilder(doc)
        builder.writeln(input)
        doc.save(f"{message.from_user.id}_output.docx")
        await msg.edit("Selesai ⬇️")
        await client.send_document(document=f"{message.from_user.id}_output.docx", chat_id=message.from_user.id)
    except Exception as e:
        await msg.edit(e)
