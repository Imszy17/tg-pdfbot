from io import BytesIO
from pyrogram import Client, filters
from pyrogram.types import Message

from database.list_user_db import add_user_list, rem_user_list, userlists


@Client.on_message(filters.command("adduser"))
async def adduserlist(client, message):
    input = " ".join(message.command[1:])
    try:
        add_user_list(int(input))
        await message.reply("`User added to list!`")
    except Exception as e:
        await message.reply("Error: " + e)

@Client.on_message(filters.command("listuser"))
async def listsuser(client, message):
    users = []
    all_user = userlists()
    for i in all_user:
        users.append(i)
    chatfile = "Daftar ID pengguna:\n"
    P = 1
    for user in users:
        try:
            chatfile += "{}. {}".format(P, user)
            P = P + 1
        except:
            pass
    with BytesIO(str.encode(chatfile)) as output:
        output.name = "userlist.txt"
        await message.reply_document(document=output, disable_notification=True)
