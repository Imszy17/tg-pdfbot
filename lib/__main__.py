from pyrogram import idle
from pyromod import Client

from config import API_HASH, API_ID, BOT_TOKEN

bot = Client(
    ":memory:",
    api_hash=API_HASH,
    api_id=API_ID,
    bot_token=BOT_TOKEN,
    plugins=dict(root="lib"),
)

bot.start()
idle()
print("Bot started!")
