from pyrogram import *
from pyrogram.types import *
import os
import re
import time
from info import API_ID, API_HASH

@Client.on_message(filters.private & filters.command("clone"))
async def clone(bot, msg: Message):
    chat = msg.chat
    text1 = await msg.reply("<b>Hᴇʏ Bʀᴏ Usᴇ Cᴏʀʀᴇᴄᴛ Mᴇᴛʜᴏᴅ\n\nEɢ : <code>/clone [bot token]</code></b>")
    cmd = msg.command
    phone = msg.command[1]
    bot_id = msg.text.split(":")[0]
    try:
        await text1.edit("<b>Tʀʏɪɴɢ Tᴏ Cᴏɴɴᴇᴄᴛ Yᴏᴜʀ Bᴏᴛ...</b>")
                  
        client = Client(bot_id + "_0", API_ID, API_HASH, bot_token=phone, plugins={"root": "Clone"})
        await client.start()
        idle()
        user = await client.get_me()
        await text1.delete()
        await msg.reply(f"<b>Hᴇʏ Bʀᴏ Yᴏᴜ Bᴏᴛ Hᴀs Bᴇᴇɴ Sᴛᴀʀᴛᴇᴅ As @{user.username} ✅ \n\nAᴅᴅ Tᴏ Yᴏᴜʀ Gʀᴏᴜᴘ Aɴᴅ Eɴᴊᴏʏ.. 📣</b>")
     
    except Exception as e:
        await text1.delete()
        await msg.reply(f"**❌ Eʀʀᴏʀ :**\n\n`{str(e)}`\n\nIғ Hᴀᴠᴇ Aɴʏ Dᴏᴜʙᴛ Asᴋ Iɴ Sᴜᴘᴘᴏʀᴛ ❗")
