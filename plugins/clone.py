from pyrogram import *
from pyrogram.types import *
from pyromod import listen
import os
import re
import time
from info import API_ID, API_HASH
from database.connections_mdb import add_bot, all_bot

@Client.on_message(filters.private & filters.command("clone") & ~filters.bot, group=3)
async def clone(bot:Client, msg:Message):
    chat = msg.chat
    post:Message = await bot.ask(chat_id=msg.from_user.id, text = "Oᴋᴀʏ Nᴏᴡ Sᴇɴᴛ Mᴇ Bᴏᴛ Tᴏᴋᴇɴ", timeout = 360)
    phone = post.text
    cmd = msg.command
    bot_id1 = post.text.split(":")[0]
    try:
        text1 = await msg.reply("<b>Tʀʏɪɴɢ Tᴏ Cᴏɴɴᴇᴄᴛ Yᴏᴜʀ Bᴏᴛ...</b>")
                  
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
            bot = await client.get_me([bot_id])
            title = bot.username
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
@Client.on_callback_query()
async def callback(client:Client, query:CallbackQuery):
    
    if "botcb" in query.data:
        await query.answer()

        bot_id = query.data.split(":")[1]

        hr = await client.get_chat(int(bot_id))
        title = hr.title
        user_id = query.from_user.id

      

        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("Dᴇʟᴇᴛᴇ", callback_data=f"deletebcb:{group_id}")],
            [InlineKeyboardButton("Bᴀᴄᴋ", callback_data="backbcb")]
        ])

        await query.message.edit_text(
            f"Bot Name :- **{title}**",
            reply_markup=keyboard,
            parse_mode=enums.ParseMode.MARKDOWN
        )
        return await query.answer('Hᴀᴘᴘʏ Aʟʟᴇ Dᴀ')
    
    
    elif "deletebcb" in query.data:
        await query.answer()

        user_id = query.from_user.id
        bot_id = query.data.split(":")[1]

        delcon = await delete_bot(str(user_id), str(bot_id))

        if delcon:
            await query.message.edit_text(
                "Successfully deleted connection"
            )
        else:
            await query.message.edit_text(
                f"Some error occurred!!",
                parse_mode=enums.ParseMode.MARKDOWN
            )
        return await query.answer('𝙿𝙻𝙴𝙰𝚂𝙴 𝚂𝙷𝙰𝚁𝙴 𝙰𝙽𝙳 𝚂𝚄𝙿𝙿𝙾𝚁𝚃')
    elif query.data == "backbcb":
        await query.answer()

        userid = query.from_user.id

        bot_ids = await all_bot(str(userid))
        if bot_ids is None:
            await query.message.edit_text(
                "There are no active connections!! Connect to some groups first.",
            )
            return await query.answer('𝙿𝙻𝙴𝙰𝚂𝙴 𝚂𝙷𝙰𝚁𝙴 𝙰𝙽𝙳 𝚂𝚄𝙿𝙿𝙾𝚁𝚃')
        buttons = []
        for bot_id in bot_ids:
            try:
                ttl = await client.get_chat(int(bot_id))
                title = ttl.username
                
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
            await query.message.edit_text(
                "Your connected group details ;\n\n",
                reply_markup=InlineKeyboardMarkup(buttons)
            )
        else:
            await query.message.edit(
                "Hello"
            )

    
   
                
                
                
                
                
