from pyrogram import Client, filters
from info import REQ_CHAT
from database.ia_filterdb import get_search_results
from utils import get_settings

@Client.on_message(filters.chat(REQ_CHAT) & filters.incoming)
async def auto_filter(client, msg, spoll=False):
    if not spoll:
        message = msg
        settings = await get_settings(message.chat.id)
        if message.text.startswith("/"): return  # ignore commands
        if re.findall("((^\/|^,|^!|^\.|^[\U0001F600-\U000E007F]).*)", message.text):
            return
        if 2 < len(message.text) < 100:
            search = message.text
            files, offset, total_results = await get_search_results(search.lower(), offset=0, filter=True)
            if not files:
                if settings["spell_check"]:
                    return await message.reply("Sᴏʀʏ I Cᴀɴᴏᴛ Fɪɴᴅ Mᴏᴠɪᴇ Iɴ Mʏ Dᴀᴛᴀʙᴀsᴇ Aɴʏ Wᴀʏ Iᴛ Wᴀsᴘ Rᴇᴘᴏʀᴛᴇᴅ Tᴏ Aᴅᴍɪɴs")
                else:
                    return await message.reply("Sᴏʀʏ I Cᴀɴᴏᴛ Fɪɴᴅ Mᴏᴠɪᴇ Iɴ Mʏ Dᴀᴛᴀʙᴀsᴇ Aɴʏ Wᴀʏ Iᴛ Wᴀsᴘ Rᴇᴘᴏʀᴛᴇᴅ Tᴏ Aᴅᴍɪɴs")
                    return
        else:
            return await message.reply(f"Hᴇʏ {message.from_user.mention} Hᴇʀᴇ Fᴏᴜɴᴅ {total_results} Rᴇsᴜʟᴛs Fᴏʀ Yᴏᴜʀ Qᴜᴇʀʏ")
