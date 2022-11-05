from pyrogram import *
from pyrogram.types import *
from plugins.clone import client
@Client.on_message(filters.command(['start']) & filters.private)
async def clone_start(bot, msg):
  me = await client.get_me()
  btn = [[
      InlineKeyboardButton('❗Hᴇʟᴘ', callback_data="help"),
      InlineKeyboardButton('😎 Aʙᴏᴜᴛ', callback_data="about")
  ]]
  await msg.reply_text(
      text = f"<b>Yᴏ Yᴏ !\nIᴀᴍ {me.username} Aɴ Sɪᴍᴘʟᴇ Aᴜᴛᴏ Fɪʟᴛᴇ + Fɪʟᴇ Sʜᴀʀᴇ Bᴏᴛ...</b>",
      reply_markup = InlineKeyboardMarkup(btn)
  )
