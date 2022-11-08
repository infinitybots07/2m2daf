from pyrogram import *
from pyrogram.types import *
import os
import re
import time
from info import API_ID, API_HASH
from database.connections_mdb import add_bot, all_bot


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
        await add_bot(str(bot_id), str(user_id))
        await text1.edit(f"<b>Hᴇʏ Bʀᴏ Yᴏᴜ Bᴏᴛ Hᴀs Bᴇᴇɴ Sᴛᴀʀᴛᴇᴅ As @{user.username} ✅ \n\nAᴅᴅ Tᴏ Yᴏᴜʀ Gʀᴏᴜᴘ Aɴᴅ Eɴᴊᴏʏ.. 📣</b>")
     
    except Exception as e:
        
        await text1.edit(f"**❌ Eʀʀᴏʀ :**\n\n`{str(e)}`\n\nIғ Hᴀᴠᴇ Aɴʏ Dᴏᴜʙᴛ Asᴋ Iɴ Sᴜᴘᴘᴏʀᴛ ❗")
        
@Client.on_message(filters.private & filters.command(["mybots"]))
async def mybots(client, message):
    user_id = message.from_user.id
    bot_ids = await all_bot(str(user_id))
    if bot_ids is None:
        await message.reply_text(
            "There are no active connections!! Connect to some groups first.",
            quote=True
        )
        return
    buttons = []
    for bot_id in bot_ids:
        try:
            ttl = bot_id
            tt2 = await client.get_chat(int(ttl))
            title = tt2.username
            buttons.append(
                [
             
                    InlineKeyboardButton(
                        text=f"{title}", callback_data=f"botcb:{bot_id}"
                    )
                ]
            )
        except:
            pass
    if buttons:
        await message.reply(
            text="Yᴏᴜʀ Cᴏɴɴᴇᴄᴛᴇᴅ Gʀᴏᴜᴘ Dᴇᴛᴀɪʟs Rᴇ Gɪᴠᴇɴ Bᴇʟᴏᴡ :\n\n",
            reply_markup=InlineKeyboardMarkup(buttons),
            quote=True
        )
    else:
        await message.reply(
            'Hey First Create A Bot Then Try Again ):',
            quote=True
        )
        
                
                
                
                
                
                
