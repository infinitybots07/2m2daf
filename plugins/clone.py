from pyrogram import Client, filters



@Client.on_message(filters.command(["clone"]))
async def clone(client, msg):
  tok = await get_text_content
  if not tok:
    return await msg.reply("I Cᴏᴜʟᴅ Nᴏᴛ Fɪɴᴅ Aɴʏ Tᴏᴋᴇɴ Lɪᴋᴇ Tʜᴀᴛ")
  
