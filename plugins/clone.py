from pyrogram import *
from pyrogram.types import *
import os
import re
import time
from info import API_ID, API_HASH
from database.connections_mdb import add_bot


@Client.on_message(filters.private & filters.command("clone"))
async def clone(bot, msg: Message):
    chat = msg.chat
    text1 = await msg.reply("<b>Hᴇʏ Bʀᴏ Usᴇ Cᴏʀʀᴇᴄᴛ Mᴇᴛʜᴏᴅ\n\nEɢ : <code>/clone [bot token]</code></b>")
    cmd = msg.command
    phone = msg.command[1]
    bot_id1 = msg.text.split(":")[0]
    try:
        await text1.edit("<b>Tʀʏɪɴɢ Tᴏ Cᴏɴɴᴇᴄᴛ Yᴏᴜʀ Bᴏᴛ...</b>")
                  
        client = Client(bot_id1 + "_0", API_ID, API_HASH, bot_token=phone, plugins={"root": "Clone"})
        await client.start()
        idle()
        user = await client.get_me()
        bot_id = user.id
        user_id = msg.from_user.id
        await text1.delete()
        await add_bot(str(bot_id), str(user_id))
        await msg.reply(f"<b>Hᴇʏ Bʀᴏ Yᴏᴜ Bᴏᴛ Hᴀs Bᴇᴇɴ Sᴛᴀʀᴛᴇᴅ As @{user.username} ✅ \n\nAᴅᴅ Tᴏ Yᴏᴜʀ Gʀᴏᴜᴘ Aɴᴅ Eɴᴊᴏʏ.. 📣</b>")
     
    except Exception as e:
        await text1.delete()
        await msg.reply(f"**❌ Eʀʀᴏʀ :**\n\n`{str(e)}`\n\nIғ Hᴀᴠᴇ Aɴʏ Dᴏᴜʙᴛ Asᴋ Iɴ Sᴜᴘᴘᴏʀᴛ ❗")
        
@Client.on_message(filters.private & filters.command("mybots"))
async def mybots(client, message):
    user_id = message.from_user.id
    bot_id = await all_bot(str(user_id))
    if bot_id:
        ttle = bot_id.title
        btn = [[
            InlineKeyboardButton(
                f'{ttle}', callback_data=f"mybot2#{bot_id}"
            )
        ]]
        await message.reply_text('Hey ! Choose A From Given Below', reply_markup=InlineKeyboardMarkup(btn))
    else:
        await message.reply_text('Hey First Create A Bot Then Try Again ):')
                
                
                
                
                
                
                
