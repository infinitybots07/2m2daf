class script(object):
    START_TXT = """<b>Hᴇʏ {} ɪᴍ Tʜᴏᴍᴀs Sʜᴇʟʙʏ ᴀɴ Aᴡᴇsᴏᴍᴇ Aᴜᴛᴏ + Mᴀɴᴜᴀʟ Fɪʟᴛᴇʀ + Fɪʟᴇ Sʜᴀʀᴇ Bᴏᴛ.</b>
    
<i>Aᴅᴅ ᴍᴇ ᴛᴏ ʏᴏᴜʀ ɢʀᴏᴜᴘ ᴛᴏ sᴇᴇ ᴛʜᴇ ᴍᴀɢɪᴄ ᴏʀ ʀᴇᴀᴅ ᴍᴏʀᴇ ғʀᴏᴍ ᴛʜᴇ ᴍᴇɴᴜ ʙᴇʟᴏᴡ</i>"""
    ABOUT_TXT = """<b>○ Mʏ Nᴀᴍᴇ : <a href=https://t.me/CL_FILTER_BOT><b>Tʜᴏᴍᴀs Sʜᴇʟʙʏ</b></a>
○ Cʀᴇᴀᴛᴏʀ : <a href=https://t.me/NL_MP4_BOT><b>ɴɪʜᴀᴀʟ 🇮🇳</b></a>
○ Lᴀɴɢᴜᴀɢᴇ : <a href=https://python.com>Pʏᴛʜᴏɴ</a>
○ Lɪʙʀᴀʀʏ : <a href=https://pyrogram.com>Pʏʀᴏɢʀᴀᴍ Asʏɴᴄɪᴏ 𝟢.𝟣𝟩.𝟣</a>
○ Sᴇʀᴠᴇʀ : <a href=www.railway.app><b>Rᴀɪʟᴡᴀʏ</b></a>
○ Dᴀᴛᴀʙᴀsᴇ : <a href=www.mangodb.com><b>MᴀɴɢᴏDB</b></a>
○ Bᴜɪʟᴅ sᴛᴀᴛᴜs : V9.8 [ Kɪʟʟᴀᴅɪ ]</b>"""

    HELP_TXT = """Hᴇʏ {} Wᴇʟᴄᴏᴍᴇ Tᴏ Mʏ Hᴇʟᴘ Iғ Yᴏᴜ Sᴇᴇᴍ Lᴏsᴛ Oʀ Hᴀᴠᴇ A Dᴏᴜʙᴛ Usᴇ Tʜᴇ Bᴜᴛᴛᴏɴs Bᴇʟᴏᴡ Tᴏ Nᴀᴠɪɢᴀᴛᴇ Tʜʀᴏᴜɢʜ Iᴛ !"""
    
    
    IMDB_MOVIE_2 = """<b>🧿 Tɪᴛᴛʟᴇ :  [{title}]({url})
🌟 Rᴀᴛɪɴɢ : <code>{rating} / 10</code>
🎭 Gᴇɴʀᴇ : <code>{genres}</code>

📆 Rᴇʟᴇᴀsᴇ : <code>{year}</code>
⏰ Dᴜʀᴀᴛɪᴏɴ : <code>{runtime} Mɪɴᴜᴛᴇs</code>
🎙️ Lᴀɴɢᴜᴀɢᴇ : <code>{language}</code>

🔖 Sʜᴏʀᴛ Sᴛᴏʀʏ : <code>{short}</code>

<i>★ Pᴏᴡᴇʀᴇᴅ Bʏ : {group}</i>
</b>"""
 
    MANUALFILTER_TXT = """<b>Mᴀɴᴜᴀʟ ғɪʟᴛᴇʀs ᴀʟʟᴏᴡ ʏᴏᴜ ᴛᴏ sᴀᴠᴇ ᴄᴜsᴛᴏᴍ ғɪʟᴛᴇʀs ᴏᴛʜᴇʀ ᴛʜᴀɴ ᴛʜᴇ ᴀᴜᴛᴏᴍᴀᴛɪᴄ ᴏɴᴇs. Fɪʟᴛᴇʀs ᴄᴀɴ ʙᴇ ᴏғ ᴛᴇxᴛ/ᴘʜᴏᴛᴏ/ᴅᴏᴄᴜᴍᴇɴᴛ/ᴀᴜᴅɪᴏ/ᴀɴɪᴍᴀᴛɪᴏɴ/ᴠɪᴅᴇᴏ</b> .

<b><u>Nᴇᴡ ғɪʟᴛᴇʀ :</b></u>

<b><u>Fᴏʀᴍᴀᴛ</b></u>

/filter "keyword" text or
Rᴇᴘʟʏ ᴛᴏ ᴀ ᴍᴇssᴀɢᴇ ->/filter "keyword"

Usᴀɢᴇ
/filter "hi" hello
[hello] -> Reply -> /filter hi

<b><u>Sᴛᴏᴘ ғɪʟᴛᴇʀ :</b></u>

Fᴏʀᴍᴀᴛ
/stop "keyword"

Usᴀɢᴇ
/stop "hi"

<b><u>Vɪᴇᴡ ғɪʟᴛᴇʀs :</b></u>

/filters"""
    
    FORCE_TXT = """**Hᴇʏ Bᴜᴅᴅʏ
    
Yᴏᴜ Wᴀɴᴛ Tᴏ Jᴏɪɴ Mʏ Cʜᴀɴɴᴇʟ Tᴏ Usᴇ Tʜɪs Bᴏᴛ 🤧**"""
    SPELL_TXT = "✯ 𝖢𝗁𝖾𝖼𝗄 𝖮𝖳𝖳 𝖱𝖾𝗅𝖾𝖺𝗌𝖾 ᴏʀ 𝖢𝗈𝗋𝗋𝖾𝖼𝗍 𝖳𝗁𝖾 𝗌𝗉𝖾𝗅𝗅𝗂𝗇𝗀\n\n✯ 𝖣𝗈𝗇𝗍 𝖴𝗌𝖾 𝖲𝗒𝗆𝖻𝗈𝗅𝗌 𝖶𝗁𝗂𝗅𝖾 𝖱𝖾𝗊𝗎𝖾𝗌𝗍 (,:'?!* 𝖾𝗍𝖼..)\n\n✯ [𝖬𝗈𝗏𝗂𝖾 𝖭𝖺𝗆𝖾 ,𝖸𝖾𝖺𝗋 ,𝖫𝖺𝗇𝗀𝗎𝖺𝗀𝖾] 𝖠𝗌𝗄 𝖳𝗁𝗂𝗌 𝖶𝖺𝗒"     
        
    BUTTON_TXT = """<u><b>Hᴇʟᴘ: Bᴜᴛᴛᴏɴs</b></u> 
    
Eᴠᴀ Mᴀʀɪᴀ Sᴜᴘᴘᴏʀᴛs ʙᴏᴛʜ ᴜʀʟ ᴀɴᴅ ᴀʟᴇʀᴛ ɪɴʟɪɴᴇ ʙᴜᴛᴛᴏɴs.
    
<u><b>NOTE:</b></u>
1. Tᴇʟᴇɢʀᴀᴍ ᴡɪʟʟ ɴᴏᴛ ᴀʟʟᴏᴡs ʏᴏᴜ ᴛᴏ sᴇɴᴅ ʙᴜᴛᴛᴏɴs ᴡɪᴛʜᴏᴜᴛ ᴀɴʏ ᴄᴏɴᴛᴇɴᴛ, sᴏ ᴄᴏɴᴛᴇɴᴛ ɪs ᴍᴀɴᴅᴀᴛᴏʀʏ.
𝟸. Bᴏᴛ sᴜᴘᴘᴏʀᴛs ʙᴜᴛᴛᴏɴs ᴡɪᴛʜ ᴀɴʏ ᴛᴇʟᴇɢʀᴀᴍ ᴍᴇᴅɪᴀ ᴛʏᴘᴇ.
𝟹. Bᴜᴛᴛᴏɴs sʜᴏᴜʟᴅ ʙᴇ ᴘʀᴏᴘᴇʀʟʏ ᴘᴀʀsᴇᴅ ᴀs ᴍᴀʀᴋᴅᴏᴡɴ ғᴏʀᴍᴀᴛ URL ʙᴜᴛᴛᴏɴs:<ᴄᴏᴅᴇ>Bᴜᴛᴛᴏɴ Tᴇxᴛ<ʙ>Aʟᴇʀᴛ ʙᴜᴛᴛᴏɴs:<ᴄᴏᴅᴇ>Bᴜᴛᴛᴏɴ Tᴇxᴛ""" 
    
    AUTOFILTER_TXT = """<b><u>Hᴇʟᴘ Fᴏʀ Aᴜᴛᴏ Fɪʟᴛᴇʀ</b></u>
    
Aᴜᴛᴏғɪʟᴛᴇʀ ᴍᴏᴅᴜʟᴇ sᴇᴀʀᴄʜᴇs ɪᴍᴅʙ ғᴏʀ ᴍᴏᴠɪᴇ ᴅᴇᴛᴀɪʟs ᴀɴᴅ ᴅʙ ғᴏʀ ғɪʟᴇs ᴀɴᴅ sᴇɴᴅs ʀᴇsᴜʟᴛs ғᴏʀ ᴇᴀᴄʜ ᴍᴇssᴀɢᴇ ɪɴ ᴀ ɢʀᴏᴜᴘ

<b><u>Cᴏᴍᴍᴀɴᴅ Aɴᴅ Usᴀɢᴇ</b></u>

Yᴏᴜ Cᴀɴ Fᴏᴜɴᴅ Oɴ/Oғғ Fᴀᴄɪʟɪᴛᴇs Iɴ /settings

Nᴏᴛᴇ :- Aᴜᴛᴏғɪʟᴛᴇʀ ɪs ᴇɴᴀʙʟᴇᴅ ʙʏ ᴅᴇғᴀᴜʟᴛ
""" 
    
    CONNECTION_TXT = """Cᴏɴɴᴇᴄᴛɪᴏɴs ᴀʟʟᴏᴡ ʏᴏᴜ ᴛᴏ ᴍᴀɴᴀɢᴇ ʏᴏᴜʀ ɢʀᴏᴜᴘ ʜᴇʀᴇ ɪɴ ᴘᴍ ɪɴsᴛᴇᴀᴅ ᴏғ sᴇɴᴅɪɴɢ ᴛʜᴏsᴇ ᴄᴏᴍᴍᴀɴᴅs ᴘᴜʙʟɪᴄʟʏ ɪɴ ᴛʜᴇ ɢʀᴏᴜᴘ ⠘⁾

<u><b>Cᴏɴɴᴇᴄᴛ :</b></u>

-> Fɪʀsᴛ ɢᴇᴛ ʏᴏᴜʀ ɢʀᴏᴜᴘ's ɪᴅ ʙʏ sᴇɴᴅɪɴɢ /id ɪɴ ʏᴏᴜʀ ɢʀᴏᴜᴘ
-> /connect [group_id]

<u><b>Dɪsᴄᴏɴɴᴇᴄᴛ :</b></u>

/disconnect"""
  
    ADMIN_TXT = """<b><u>Hᴇʟᴘ: Aᴅᴍɪɴ Mᴏᴅᴇ</b></u>
<b><u>Nᴏᴛᴇ</b></u>

Tʜɪs Mᴏᴅᴜʟᴇ Oɴʟʏ Wᴏʀᴋ Fᴏʀ Aᴅᴍɪɴ :)

<b><u>Cᴏᴍᴍᴀɴᴅ Aɴᴅ Usᴀɢᴇ :</b></u>

• /logs - <code>to get the rescent errors</code>
• /stats - <code>to get status of files in db.</code>
• /delete - <code>to delete a specific file from db.</code>
• /users - <code>to get list of my users and ids.</code>
• /chats - <code>to get list of the my chats and ids </code>
• /leave  - <code>to leave from a chat.</code>
• /disable  -  <code>do disable a chat.</code>
• /ban  - <code>to ban a user.</code>
• /unban  - <code>to unban a user.</code>
• /channel - <code>to get list of total connected channels</code>
• /broadcast - <code>to broadcast a message to all users</code>"""
    
    STATUS_TXT = """<b><u>Cᴜʀʀᴇɴᴛ Dᴀᴛᴀʙᴀsᴇ Sᴛᴀᴛᴜs</b></u>
    
📑 ғɪʟᴇs sᴀᴠᴇᴅ: <code>{}</code>
👩🏻‍💻 ᴜsᴇʀs: <code>{}</code>
👥 ɢʀᴏᴜᴘs: <code>{}</code>
🗂️ ᴏᴄᴄᴜᴘɪᴇᴅ: <code>{}</code>
⚒️ Cᴜsᴛᴏᴍɪᴢᴇᴅ Cʜᴀᴛs : <code>{}</code>
📖 Mᴀɴᴜᴀʟ Fɪʟᴛᴇʀs : <code>{}</code>
"""
    
    JSON_TXT = """<u><b>Hᴇʟᴘ Fᴏʀ Jsᴏɴ </b></u>
  
Bᴏᴛ Rᴇᴛᴜʀɴ Jsᴏɴ Tᴏ Aʟʟ Mᴇssᴀɢᴇs /json

<b><u>Mᴇssᴀɢᴇ Eᴅɪᴛɪɴɢ Jsᴏɴ Oɴ :</u></b>

• Pᴍ Sᴜᴘᴘᴏʀᴛ
• Gʀᴏᴜᴘ Sᴜᴘᴘᴏʀᴛ

<b><u>Nᴏᴛᴇ :</u></b>

Tʜɪs Fᴇᴀᴛᴜʀᴇ Wɪʟʟ Wᴏʀᴋ Fᴏʀ Eᴠᴇʀʏᴏɴᴇ
"""
    
    LOG_TEXT_G = """#NewGroup
Group = {}(<code>{}</code>)
Total Members = <code>{}</code>
Added By - {}
"""
    LOG_TEXT_P = """#NewUser
ID - <code>{}</code>
Name - {}
"""
    

