from pyrogram import Client, filters, errors
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import os
from info import API_ID, API_HASH
from pyrogram.handlers import MessageHandler
import plugins.pm_filter as pm

clients = []

async def start_message(msg):
    me = await msg.get_me()
    return await msg.reply(f"Hello Im, @{me.username}, running in cloneMode.")


def load_handlers(bot):
    bot.add_handler(MessageHandler(start_message, filters.command('start')))
    
async def bt_clone(client, update):
    btid = update.text.split(":")[0]
    btclient = Client(btid + "-0", API_ID, API_HASH)
    clients.append(btclient)
    try:
        await btclient.start(update)
    except Exception as e:
        return str(e)
    load_handlers(btclient)
    return""

async def get_text_content(message):
    """Returns the text content of a message."""
    if message.reply_to_message_id:
        reply = await message.get_message()
        if reply.media:
            if reply.document:
                doc = await reply.download_media()
                with open(doc, "r", errors="ignore") as f:
                    u = f.read()
                os.remove(doc)
                return u
            else:
                return None
        else:
            return reply.text
    else:
        try:
            return message.text.split(" ", 1)[1]
        except:
            return None

@Client.on_message((filters.private | filters.group) & filters.command('clone'))
async def clone(client, msg):
  tok = await get_text_content(msg)
  if not tok:
    return await msg.reply("I Cᴏᴜʟᴅ Nᴏᴛ Fɪɴᴅ Aɴʏ Tᴏᴋᴇɴ Lɪᴋᴇ Tʜᴀᴛ")
  add = await bt_clone(tok)
  if add != "":
      return await msg.reply(add)
  return await msg.reply("Bᴏᴛ Hᴀs Bᴇᴇɴ Cᴏɴɴᴇᴄᴛᴇᴅ 🙌")
    
  
