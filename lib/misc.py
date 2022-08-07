from pyrogram import Client, filters
from pyrogram.types import Message

from database.list_user_db import add_user_list, rem_user_list


@Client.on_message(filters.command("adduser"))
async def adduserlist(client, message):
    input = " ".join(message.command[1:])
    try:
        add_user_list(int(input))
        await message.reply("`User added to list!`")
    except Exception as e:
        await message.reply("Error: " + e)
