from pyrogram import *
from pyrogram.types import *
import os
import re
import time
from info import API_ID, API_HASH

@Client.on_message(filters.private & filters.command("clone"))
async def clone(bot, msg: Message):
    chat = msg.chat
    text = await msg.reply("<b>Hᴇʏ Bʀᴏ Usᴇ Cᴏʀʀᴇᴄᴛ Mᴇᴛʜᴏᴅ\n\nEɢ : <code>/clone [bot token]</code></b>")
    cmd = msg.command
    phone = msg.command[1]
    try:
        await text.edit("<b>Tʀʏɪɴɢ Tᴏ Cᴏɴɴᴇᴄᴛ Yᴏᴜʀ Bᴏᴛ...</b>")
                   # change this Directry according to ur repo
        client = Client(":memory:", API_ID, API_HASH, bot_token=phone, plugins={"root": "Clone"})
        await client.start()
        user = await client.get_me()
        await msg.reply(f"<b>Hᴇʏ Bʀᴏ Yᴏᴜ Bᴏᴛ Hᴀs Bᴇᴇɴ Sᴛᴀʀᴛᴇᴅ As @{user.username} ✅ \n\nAᴅᴅ Tᴏ Yᴏᴜʀ Gʀᴏᴜᴘ Aɴᴅ Eɴᴊᴏʏ.. 📣</b>")
        CLONE_NAME = user.username
        await Client.send_message(CLONE_NAME, "/start")
    except Exception as e:
        await msg.reply(f"**❌ Eʀʀᴏʀ :**\n\n`{str(e)}`\n\nIғ Hᴀᴠᴇ Aɴʏ Dᴏᴜʙᴛ Asᴋ Iɴ Sᴜᴘᴘᴏʀᴛ ❗")
