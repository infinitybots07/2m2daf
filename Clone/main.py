from pyrogram import Client, filters


@Client.on_message(filters.command(['start']) & filters.private)
async def clone_start(client, msg):
  await msg.reply_text(
      text = "Hi"
  )
