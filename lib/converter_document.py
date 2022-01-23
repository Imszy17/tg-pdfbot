from pyrogram.types import Message
from pyrogram import Client, filters

from aspose import words
from pyromod import listen


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
    input = await client.ask(msg.chat.id,'Silahkan Tulis dan kirim teks yang akan dikonversi!', filters=filters.text, parse_mode='Markdown', disable_web_page_preview=True)
    msg = await message.reply("Memproses...")
    # Blank document
    doc = words.Document()
    # Write a document
    try:
        builder = words.DocumentBuilder(doc)
        builder.writeln(input.text)
        doc.save(f"{message.from_user.id}_output.docx")
        await msg.edit("Selesai ⬇️")
        await client.send_document(document=f"{message.from_user.id}_output.docx", chat_id=message.from_user.id)
    except Exception as e:
        await msg.edit(e)
