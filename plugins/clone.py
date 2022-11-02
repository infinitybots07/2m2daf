from pyrogram import Client, filters, errors
import os
from info import API_ID, API_HASH
from pyrogram.handlers import MessageHandler

clients = []

async def start_(msg):
    me = await msg.Client.get_me()
    return await msg.reply(f"Hello Im, @{me.username}, running in cloneMode.")


def load_handlers(bot):
    bot.add_handler(MessageHandler(start_, filters.command('start')))

async def addBot(token):
    botID = token.split(":")[0]
    tgClient = Client(botID + "-0", API_ID, API_HASH)
    clients.append(tgClient)
    try:
        await Client.start(token)
    except Exception as err:
        return str(err)
    load_handlers(tgClient)
    return ""

async def get_text_content(message):
    """Returns the text content of a message."""
    if message.reply_to_message_id:
        reply = await message.get_reply_message()
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
  add = await addBot(tok)
  if add != "":
    return await msg.reply(add)
  return await msg.reply("connected")
    
  
