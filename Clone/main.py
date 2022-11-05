from pyrogram import *
from pyrogram.types import *
from plugins.pm_filter import auto_filter, manual_filter

@Client.on_message(filters.command(['start']) & filters.private)
async def clone_start(bot, msg):
 
  btn = [[
      InlineKeyboardButton('❗Hᴇʟᴘ', callback_data="c_help"),
      InlineKeyboardButton('😎 Aʙᴏᴜᴛ', callback_data="c_about")
  ]]
  await msg.reply_text(
      text = f"<b>Yᴏ Yᴏ !\nIᴀᴍ A Sɪᴍᴘʟᴇ Aᴜᴛᴏ Fɪʟᴛᴇ + Fɪʟᴇ Sʜᴀʀᴇ Bᴏᴛ...</b>",
      reply_markup = InlineKeyboardMarkup(btn)
  )

  
@Client.on_message(filters.group & filters.text & filters.incoming)
async def give_filter2(client, message):
    k = await manual_filters(client, message)
    if k == False:
        await auto_filter(client, message)  
  
  
@Client.on_callback_query()
async def cb_handler2(client: Client, query: CabllbackQuery):
    if query.data = "c_help":
        btn = [[
            InlineKeyboardButton('Bᴀᴄᴋ', callback_data="c_start")
        ]]
        await query.message.edit_text("Coming Soon..", reply_markup=InlineKeyboardMarkup(btn), parse_mode=enums.ParseMode.HTML)
    elif query.data = "c_about":
        btn = [[
            InlineKeyboardButton('Bᴀᴄᴋ', callback_data="c_start")
        ]]
        await query.message.edit_text("Coming Soon..", reply_markup=InlineKeyboardMarkup(btn), parse_mode=enums.ParseMode.HTML)
    elif query.data = "c_start":
        btn = [[
            InlineKeyboardButton('❗Hᴇʟᴘ', callback_data="c_help"),
            InlineKeyboardButton('😎 Aʙᴏᴜᴛ', callback_data="c_about")
        ]]
        await query.message.edit_text(
            text = f"<b>Yᴏ Yᴏ !\nIᴀᴍ A Sɪᴍᴘʟᴇ Aᴜᴛᴏ Fɪʟᴛᴇ + Fɪʟᴇ Sʜᴀʀᴇ Bᴏᴛ...</b>",
            reply_markup = InlineKeyboardMarkup(btn)
        )
       
       
       
       
       
       
       
       
       
       
     
     
     
     
     
     
     
