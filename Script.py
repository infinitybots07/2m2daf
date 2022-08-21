class script(object):
    START_TXT = """<b>Hᴇʏ {} ɪᴍ Tʜᴏᴍᴀs Sʜᴇʟʙʏ ᴀɴ Aᴡᴇsᴏᴍᴇ Aᴜᴛᴏ + Mᴀɴᴜᴀʟ Fɪʟᴛᴇʀ + Fɪʟᴇ Sʜᴀʀᴇ Bᴏᴛ.</b>
    
<i>Aᴅᴅ ᴍᴇ ᴛᴏ ʏᴏᴜʀ ɢʀᴏᴜᴘ ᴛᴏ sᴇᴇ ᴛʜᴇ ᴍᴀɢɪᴄ ᴏʀ ʀᴇᴀᴅ ᴍᴏʀᴇ ғʀᴏᴍ ᴛʜᴇ ᴍᴇɴᴜ ʙᴇʟᴏᴡ</i>"""
    ABOUT_TXT = """<b>○ Mʏ Nᴀᴍᴇ : <a href=https://t.me/CL_FILTER_BOT><b>Tʜᴏᴍᴀs Sʜᴇʟʙʏ</b></a>
○ Cʀᴇᴀᴛᴏʀ : <a href=https://t.me/NL_MP4_BOT><b>ɴɪʜᴀᴀʟ 🇮🇳</b></a>
○ Lᴀɴɢᴜᴀɢᴇ : Pʏᴛʜᴏɴ 𝟥 
○ Lɪʙʀᴀʀʏ : Pʏʀᴏɢʀᴀᴍ Asʏɴᴄɪᴏ 𝟢.𝟣𝟩.𝟣 
○ Sᴇʀᴠᴇʀ : Hᴇʀᴏᴋᴜ
○ Dᴀᴛᴀʙᴀsᴇ : <a href=www.mangodb.com><b>MᴀɴɢᴏDB</b></a>
○ Bᴜɪʟᴅ sᴛᴀᴛᴜs : V9.8 [ Kɪʟʟᴀᴅɪ ]</b>"""

    HELP_TXT = """Hᴇʏ {} Wᴇʟᴄᴏᴍᴇ Tᴏ Mʏ Hᴇʟᴘ Iғ Yᴏᴜ Sᴇᴇᴍ Lᴏsᴛ Oʀ Hᴀᴠᴇ A Dᴏᴜʙᴛ Usᴇ Tʜᴇ Bᴜᴛᴛᴏɴs Bᴇʟᴏᴡ Tᴏ Nᴀᴠɪɢᴀᴛᴇ Tʜʀᴏᴜɢʜ Iᴛ !"""
    
    
    IMDB_MOVIE_2 = """<b>
🧿 ᴛɪᴛᴛʟᴇ :  [{title}]({url})
🌟 ʀᴀᴛɪɴɢ : <code>{rating} / 10</code>
🎭 ɢᴇɴʀᴇ : <code>{genres}</code>

📆 ʀᴇʟᴇᴀsᴇ : <code>{year}</code>
⏰ ᴅᴜʀᴀᴛɪᴏɴ : <code>{runtime} Mɪɴᴜᴛᴇs</code>
🎙️ ʟᴀɴɢᴜᴀɢᴇ : <code>{language}</code>

🔖 sʜᴏʀᴛ Sᴛᴏʀʏ : <code>{short}</code>

<i>★ ᴘᴏᴡᴇʀᴇᴅ ʙʏ : {group}</i>
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
    BUTTON_TXT = """<u><b>Hᴇʟᴘ: Bᴜᴛᴛᴏɴs</b></u> 
    
Eᴠᴀ Mᴀʀɪᴀ Sᴜᴘᴘᴏʀᴛs ʙᴏᴛʜ ᴜʀʟ ᴀɴᴅ ᴀʟᴇʀᴛ ɪɴʟɪɴᴇ ʙᴜᴛᴛᴏɴs.
    
<u><b>NOTE:</b></u>
1. Tᴇʟᴇɢʀᴀᴍ ᴡɪʟʟ ɴᴏᴛ ᴀʟʟᴏᴡs ʏᴏᴜ ᴛᴏ sᴇɴᴅ ʙᴜᴛᴛᴏɴs ᴡɪᴛʜᴏᴜᴛ ᴀɴʏ ᴄᴏɴᴛᴇɴᴛ, sᴏ ᴄᴏɴᴛᴇɴᴛ ɪs ᴍᴀɴᴅᴀᴛᴏʀʏ.
𝟸. Bᴏᴛ sᴜᴘᴘᴏʀᴛs ʙᴜᴛᴛᴏɴs ᴡɪᴛʜ ᴀɴʏ ᴛᴇʟᴇɢʀᴀᴍ ᴍᴇᴅɪᴀ ᴛʏᴘᴇ.
𝟹. Bᴜᴛᴛᴏɴs sʜᴏᴜʟᴅ ʙᴇ ᴘʀᴏᴘᴇʀʟʏ ᴘᴀʀsᴇᴅ ᴀs ᴍᴀʀᴋᴅᴏᴡɴ ғᴏʀᴍᴀᴛ URL ʙᴜᴛᴛᴏɴs:<ᴄᴏᴅᴇ>Bᴜᴛᴛᴏɴ Tᴇxᴛ<ʙ>Aʟᴇʀᴛ ʙᴜᴛᴛᴏɴs:<ᴄᴏᴅᴇ>Bᴜᴛᴛᴏɴ Tᴇxᴛ""" 
    
    AUTOFILTER_TXT = """<b><u>Hᴇʟᴘ Fᴏʀ Aᴜᴛᴏ Fɪʟᴛᴇʀ</b></u>
    
Aᴜᴛᴏғɪʟᴛᴇʀ ᴍᴏᴅᴜʟᴇ sᴇᴀʀᴄʜᴇs ɪᴍᴅʙ ғᴏʀ ᴍᴏᴠɪᴇ ᴅᴇᴛᴀɪʟs ᴀɴᴅ ᴅʙ ғᴏʀ ғɪʟᴇs ᴀɴᴅ sᴇɴᴅs ʀᴇsᴜʟᴛs ғᴏʀ ᴇᴀᴄʜ ᴍᴇssᴀɢᴇ ɪɴ ᴀ ɢʀᴏᴜᴘ

<b><u>Cᴏᴍᴍᴀɴᴅ Aɴᴅ Usᴀɢᴇ</b></u>

Eɴᴀʙʟᴇ : <code>/autofilter on</code>
Dɪsᴀʙʟᴇ : <code>/autofilter off</code>

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
"""
    
    JSON_TXT = """<u><b>Hᴇʟᴘ Fᴏʀ Jsᴏɴ </b></u>
  
Bᴏᴛ Rᴇᴛᴜʀɴ Jsᴏɴ Tᴏ Aʟʟ Mᴇssᴀɢᴇs

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
    

