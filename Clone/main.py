from pyrogram import Client, filters
from utils import temp
from pyrogram.types import *

@Client.on_message(filters.command(['start']) & filters.private)
async def clone_start(client, msg):
  btn = [[
      InlineKeyboardButton('❗Hᴇʟᴘ', callback_data="help"),
      InlineKeyboardButton('😎 Aʙᴏᴜᴛ', callback_data="about")
  ]]
  await msg.reply_text(
      text = f"<b>Yᴏ Yᴏ !\nIᴀᴍ {temp.B_NAME} Aɴ Sɪᴍᴘʟᴇ Aᴜᴛᴏ Fɪʟᴛᴇ + Fɪʟᴇ Sʜᴀʀᴇ Bᴏᴛ...</b>",
      reply_markup = InlineKeyboardMarkup(btn)
  )
