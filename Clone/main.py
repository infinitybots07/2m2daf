
import psutil
import asyncio
import re
import ast
import random
import datetime
import pytz
import math
from pyrogram.errors.exceptions.bad_request_400 import MediaEmpty, PhotoInvalidDimensions, WebpageMediaEmpty
from Script import script
import pyrogram
from database.connections_mdb import active_connection, all_connections, delete_connection, if_active, make_active, \
    make_inactive
from info import ADMINS, PICS_RT, AUTH_CHANNEL, AUTH_USERS, CUSTOM_FILE_CAPTION, AUTH_GROUPS, P_TTI_SHOW_OFF, IMDB, \
    SINGLE_BUTTON, SPELL_CHECK_REPLY, IMDB_TEMPLATE, DELETE_TIME, CH_FILTER, CH_LINK, UNAUTHORIZED_CALLBACK_TEXT, REQ_PIC, \
    AUTO_FILTER
from pyrogram import *
from pyrogram.types import *
from pyrogram.errors import FloodWait, UserIsBlocked, MessageNotModified, PeerIdInvalid
from utils import get_size, get_poster, search_gagala, temp, get_settings, save_group_settings
from database.users_chats_db import db
from database.ia_filterdb import Media, get_file_details, get_search_results
from database.filters_mdb import (
    filter_stats,
    del_all,
    find_filter,
    get_filters,
)
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.ERROR)

BUTTONS = {}
SPELL_CHECK = {}

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
  
@Client.on_callback_query(filters.regex(r"^next"))
async def next_page(bot, query):
    ident, req, key, offset = query.data.split("_")
    if int(req) not in [query.from_user.id, 0]:
        return await query.answer(UNAUTHORIZED_CALLBACK_TEXT, show_alert=True)
    try:
        offset = int(offset)
    except:
        offset = 0
    search = BUTTONS.get(key)
    if not search:
        await query.answer("You are using one of my old messages, please send the request again.", show_alert=True)
        return

    files, n_offset, total = await get_search_results(search, offset=offset, filter=True)
    try:
        n_offset = int(n_offset)
    except:
        n_offset = 0

    if not files:
        return
    settings = await get_settings(query.message.chat.id)
    if settings['button']:
        btn = [
            [
                InlineKeyboardButton(
                    text=f"⊹ {get_size(file.file_size)} ‣ {file.file_name}", callback_data=f'file#{file.file_id}#{query.from_user.id if query.from_user is not None else 0}'),
            ]
            for file in files
        ]
    else:
        btn = [
            [
                InlineKeyboardButton(
                    text=f"• {file.file_name}", callback_data=f'file#{file.file_id}#{query.from_user.id if query.from_user is not None else 0}'
                ),
                InlineKeyboardButton(
                    text=f"➪ {get_size(file.file_size)}",
                    callback_data=f'file#{file.file_id}#{query.from_user.id if query.from_user is not None else 0}',
                ),
            ]
            for file in files
        ]

    btn.insert(0, 
        [
            InlineKeyboardButton(f'Fɪʟᴇs: {len(files)}', 'dupe'),
            InlineKeyboardButton(f'Mᴏᴠɪᴇ', 'dupe'),
            InlineKeyboardButton(f'Sᴇʀɪᴇꜱ', 'dupe')
        ]
    )
   

    if 0 < offset <= 7:
        off_set = 0
    elif offset == 0:
        off_set = None
    else:
        off_set = offset - 7
    if n_offset == 0:
        btn.append(
            [InlineKeyboardButton("Pᴀɢᴇs", callback_data="pages"),
             InlineKeyboardButton(text=f"{math.ceil(int(offset) / 10) + 1} - {math.ceil(total / 10)}", callback_data="pages"),
             InlineKeyboardButton("• Bᴀᴄᴋ", callback_data=f"next_{req}_{key}_{off_set}")]
        )
       
    elif off_set is None:
        btn.append(
            [
                InlineKeyboardButton("Pᴀɢᴇs", callback_data="pages"),
                InlineKeyboardButton(text=f"{math.ceil(int(offset) / 10) + 1} - {math.ceil(total / 10)}", callback_data="pages"),
                InlineKeyboardButton("Nᴇxᴛ •", callback_data=f"next_{req}_{key}_{n_offset}")]
        )
        
    else:
        btn.append(
            [
                InlineKeyboardButton("• Bᴀᴄᴋ", callback_data=f"next_{req}_{key}_{off_set}"),
                InlineKeyboardButton(text=f"{math.ceil(int(offset) / 10) + 1} - {math.ceil(total / 10)}", callback_data="pages"),
                InlineKeyboardButton("Nᴇxᴛ •", callback_data=f"next_{req}_{key}_{n_offset}")]
        )
        
    try:
        await query.edit_message_reply_markup(
            reply_markup=InlineKeyboardMarkup(btn)
        )
    except MessageNotModified:
        pass
    await query.answer(f'⍟ Pᴀɢᴇ Nᴏ : {math.ceil(int(offset) / 10) + 1} / {math.ceil(total / 10)} ⍟ Tᴏᴛᴀʟ Rᴇsᴜʟᴛs : {len(files)}')


@Client.on_callback_query(filters.regex(r"^spolling"))
async def advantage_spoll_choker(bot, query):
    _, user, movie_ = query.data.split('#')
    if int(user) != 0 and query.from_user.id != int(user):
        return await query.answer(UNAUTHORIZED_CALLBACK_TEXT, show_alert=True)
    if movie_ == "close_spellcheck":
        return await query.message.delete()
    movies = SPELL_CHECK.get(query.message.reply_to_message_id)
    if not movies:
        return await query.answer("Aʜʜ Bᴜᴛᴛᴏɴ Exᴘɪʀᴇᴅ 😒", show_alert=True)
    movie = movies[(int(movie_))]
    await query.answer('Wᴀɪᴛ Cʜᴇᴄᴋɪɴɢ...')
    k = await manual_filters(bot, query.message, text=movie)
    if k == False:
        files, offset, total_results = await get_search_results(movie, offset=0, filter=True)
        if files:
            k = (movie, files, offset, total_results)
            await auto_filter(bot, query, k)
        else:
            btn = [
                [
                    InlineKeyboardButton(
                        '➕ ᴀᴅᴅ ʙᴏᴛ ᴛᴏ ʏᴏᴜʀ ɢʀᴏᴜᴘ ➕', url=f'http://t.me/{temp.U_NAME}?startgroup=true'
                    )
                ],
                [
                    InlineKeyboardButton(
                        "🗣️ Rᴇǫᴜᴇsᴛ Hᴇʀᴇ", url="t.me/cinema_lookam"
                    ),
                    InlineKeyboardButton(
                        "📣 Mᴏᴠɪᴇ Uᴘᴅᴀᴛᴇ", url="t.me/CL_UPDATE"
                    )
                ]
            ]
            await query.message.edit_text(f"Hᴇʏ {query.from_user.mention} Bᴜᴅᴅʏ ᴛʜɪs ᴍᴏᴠɪᴇ ɪs ɴᴏᴛ ʏᴇᴛ ʀᴇʟᴇᴀsᴇᴅ ᴏʀ ᴀᴅᴅᴇᴅ ᴛᴏ ᴍʏ ᴅᴀᴛᴀʙᴀsᴇ", reply_markup=InlineKeyboardMarkup(btn))            
            

@Client.on_callback_query()
async def cb_handler2(client: Client, query: CallbackQuery):
 
    if query.data == "close_data":
        await query.message.delete()
    elif query.data == "delallconfirm":
        userid = query.from_user.id
        chat_type = query.message.chat.type

        if chat_type == enums.ChatType.PRIVATE:
            grpid = await active_connection(str(userid))
            if grpid is not None:
                grp_id = grpid
                try:
                    chat = await client.get_chat(grpid)
                    title = chat.title
                except:
                    await query.message.edit_text("Make sure I'm present in your group!!", quote=True)
                    return await query.answer('Pᴇᴠᴇʀ Aʟʟᴇ')
            else:
                await query.message.edit_text(
                    "I'm not connected to any groups!\nCheck /connections or connect to any groups",
                    quote=True
                )
                return
        elif chat_type in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
            grp_id = query.message.chat.id
            title = query.message.chat.title

        else:
            return

        st = await client.get_chat_member(grp_id, userid)
        if (st.status == enums.ChatMemberStatus.OWNER) or (str(userid) in ADMINS):
            await del_all(query.message, grp_id, title)
        else:
            await query.answer("You need to be Group Owner or an Auth User to do that!", show_alert=True)
    elif query.data == "delallcancel":
        userid = query.from_user.id
        chat_type = query.message.chat.type

        if chat_type == enums.ChatType.PRIVATE:
            await query.message.reply_to_message.delete()
            await query.message.delete()

        elif chat_type in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
            grp_id = query.message.chat.id
            st = await client.get_chat_member(grp_id, userid)
            if (st.status == enums.ChatMemberStatus.OWNER) or (str(userid) in ADMINS):
                await query.message.delete()
                try:
                    await query.message.reply_to_message.delete()
                except:
                    pass
            else:
                await query.answer("Hᴇʏ Mᴀʜɴ Dᴏɴᴛ Tᴏᴜᴄʜ Oᴛʜᴇʀs Pʀᴏᴘᴇʀᴛɪᴇs 😁", show_alert=True)
    elif "groupcb" in query.data:
        await query.answer()

        group_id = query.data.split(":")[1]

        act = query.data.split(":")[2]
        hr = await client.get_chat(int(group_id))
        title = hr.title
        user_id = query.from_user.id

        if act == "":
            stat = "Cᴏɴɴᴇᴄᴛ"
            cb = "connectcb"
        else:
            stat = "Dɪsᴄᴏɴɴᴇᴄᴛ"
            cb = "disconnect"

        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton(f"{stat}", callback_data=f"{cb}:{group_id}"),
             InlineKeyboardButton("Dᴇʟᴇᴛᴇ", callback_data=f"deletecb:{group_id}")],
            [InlineKeyboardButton("Bᴀᴄᴋ", callback_data="backcb")]
        ])

        await query.message.edit_text(
            f"Gʀᴏᴜᴘ Nᴀᴍᴇ :- **{title}**\nGʀᴏᴜᴘ Iᴅ :- `{group_id}`",
            reply_markup=keyboard,
            parse_mode=enums.ParseMode.MARKDOWN
        )
        return await query.answer('Hᴀᴘᴘʏ Aʟʟᴇ Dᴀ')
    elif "connectcb" in query.data:
        await query.answer()

        group_id = query.data.split(":")[1]
        hr = await client.get_chat(int(group_id))

        title = hr.title
        user_id = query.from_user.id

        mkinact = await make_inactive(str(user_id))

        if mkinact:
            await query.message.edit_text(
                f"Disconnected from **{title}**",
                parse_mode=enums.ParseMode.MARKDOWN
            )
        else:
            await query.message.edit_text(
                f"Some error occurred!!",
                parse_mode=enums.ParseMode.MARKDOWN
            )
        return
    elif "deletecb" in query.data:
        await query.answer()

        user_id = query.from_user.id
        group_id = query.data.split(":")[1]

        delcon = await delete_connection(str(user_id), str(group_id))

        if delcon:
            await query.message.edit_text(
                "Successfully deleted connection"
            )
        else:
            await query.message.edit_text(
                f"Some error occurred!!",
                parse_mode=enums.ParseMode.MARKDOWN
            )
        return await query.answer('𝙿𝙻𝙴𝙰𝚂𝙴 𝚂𝙷𝙰𝚁𝙴 𝙰𝙽𝙳 𝚂𝚄𝙿𝙿𝙾𝚁𝚃')
    elif query.data == "backcb":
        await query.answer()

        userid = query.from_user.id

        groupids = await all_connections(str(userid))
        if groupids is None:
            await query.message.edit_text(
                "There are no active connections!! Connect to some groups first.",
            )
            return await query.answer('𝙿𝙻𝙴𝙰𝚂𝙴 𝚂𝙷𝙰𝚁𝙴 𝙰𝙽𝙳 𝚂𝚄𝙿𝙿𝙾𝚁𝚃')
        buttons = []
        for groupid in groupids:
            try:
                ttl = await client.get_chat(int(groupid))
                title = ttl.title
                active = await if_active(str(userid), str(groupid))
                act = "✅" if active else ""
                buttons.append(
                    [
                        InlineKeyboardButton(
                            text=f"{title} {act}", callback_data=f"groupcb:{groupid}:{act}"
                        )
                    ]
                )
            except:
                pass
        if buttons:
            await query.message.edit_text(
                "Your connected group details ;\n\n",
                reply_markup=InlineKeyboardMarkup(buttons)
            )
    elif "alertmessage" in query.data:
        grp_id = query.message.chat.id
        i = query.data.split(":")[1]
        keyword = query.data.split(":")[2]
        reply_text, btn, alerts, fileid = await find_filter(grp_id, keyword)
        if alerts is not None:
            alerts = ast.literal_eval(alerts)
            alert = alerts[int(i)]
            alert = alert.replace("\\n", "\n").replace("\\t", "\t")
            await query.answer(alert, show_alert=True)
    if query.data.startswith("file"):
        ident, file_id, rid = query.data.split("#")

        if int(rid) not in [query.from_user.id, 0]:
            return await query.answer(UNAUTHORIZED_CALLBACK_TEXT, show_alert=True)

        files_ = await get_file_details(file_id)
        if not files_:
            return await query.answer('No such file exist.')
        files = files_[0]
        title = files.file_name
        size = get_size(files.file_size)
        mention = query.from_user.mention if query.from_user else "Anounymous"
        f_caption = files.caption
        settings = await get_settings(query.message.chat.id)
        if CUSTOM_FILE_CAPTION:
            try:
                f_caption = CUSTOM_FILE_CAPTION.format(file_name='' if title is None else title,
                                                       file_size='' if size is None else size,
                                                       file_caption='' if f_caption is None else f_caption)                                                      
            except Exception as e:
                logger.exception(e)
            f_caption = f_caption
        if f_caption is None:
            f_caption = f"{files.file_name}"
        btn = [
            [
                InlineKeyboardButton(
                    '➕ ᴀᴅᴅ ʙᴏᴛ ᴛᴏ ʏᴏᴜʀ ɢʀᴏᴜᴘ ➕', url=f'http://t.me/{temp.U_NAME}?startgroup=true'
                )
            ]
        ]
        try:
            if AUTH_CHANNEL and not await is_subscribed(client, query):
                await query.answer(url=f"https://t.me/{temp.U_NAME}?start={ident}_{file_id}")
                return
            elif settings['botpm']:
                await query.answer(url=f"https://t.me/{temp.U_NAME}?start={ident}_{file_id}")
                return
            else:
                await query.answer(url=f"https://t.me/{temp.U_NAME}?start={ident}_{file_id}")
              
            
         
            
        except UserIsBlocked:
            await query.answer('Unblock the bot mahn !', show_alert=True)
        except PeerIdInvalid:
            await query.answer(url=f"https://t.me/{temp.U_NAME}?start={ident}_{file_id}")
        except Exception as e:
            await query.answer(url=f"https://t.me/{temp.U_NAME}?start={ident}_{file_id}")
 
    elif query.data == "c_help":
        btn = [[
            InlineKeyboardButton('Bᴀᴄᴋ', callback_data="c_start")
        ]]
        await query.message.edit_text("Coming Soon..", reply_markup=InlineKeyboardMarkup(btn), parse_mode=enums.ParseMode.HTML)
    elif query.data == "c_about":
        btn = [[
            InlineKeyboardButton('Bᴀᴄᴋ', callback_data="c_start")
        ]]
        await query.message.edit_text("Coming Soon..", reply_markup=InlineKeyboardMarkup(btn), parse_mode=enums.ParseMode.HTML)
    elif query.data == "c_start":
        btn = [[
            InlineKeyboardButton('❗Hᴇʟᴘ', callback_data="c_help"),
            InlineKeyboardButton('😎 Aʙᴏᴜᴛ', callback_data="c_about")
        ]]
        await query.message.edit_text(
            text = f"<b>Yᴏ Yᴏ !\nIᴀᴍ A Sɪᴍᴘʟᴇ Aᴜᴛᴏ Fɪʟᴛᴇ + Fɪʟᴇ Sʜᴀʀᴇ Bᴏᴛ...</b>",
            reply_markup = InlineKeyboardMarkup(btn)
        )
 
    elif query.data == "pages":
        
        await query.answer('Eɴᴛʜᴀᴅᴀ Mᴡᴏɴᴇ Nᴏᴋᴜɴɴᴀ 🙌')
        
  
    elif query.data == "connect":
        st = await client.get_chat_member(query.message.chat.id, query.from_user.id)
        if (
                st.status != enums.ChatMemberStatus.ADMINISTRATOR
                and st.status != enums.ChatMemberStatus.OWNER
                and str(query.from_user.id) not in ADMINS
        ):
            return
        await query.message.edit_text(
            text = '<b>• Fɪʀsᴛ Aᴅᴅ Bᴏᴛ Tᴏ Yᴏᴜʀ Gʀᴏᴜᴘ Aɴᴅ Mᴀᴋᴇ Aᴅᴍɪɴ\n\n• Tʜᴇɴ Tᴀᴋᴇ Yᴏᴜʀ Gʀᴏᴜᴘ Iᴅ\n\n• Tʜᴇɴ Cᴏᴍᴇ Bᴀᴄᴋ Tᴏ Bᴏᴛ Pᴍ\n\n• Tʜᴇɴ Sᴇɴᴛ " /connect [Cʜᴀᴛ Iᴅ]\n\nEɢ : \n/connect -100*******</b>',
            reply_markup = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton('❌ Cʟᴏsᴇ', callback_data='close_data')
                    ]
                ]
            ),
            parse_mode=enums.ParseMode.HTML
        )
        
    elif query.data == "moviis":  
        await query.answer("⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯\nʀᴇǫᴜᴇꜱᴛ ꜰᴏʀᴍᴀᴛ\n⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯\n\nɢᴏ ᴛᴏ ɢᴏᴏɢʟᴇ ➠ ᴛʏᴘᴇ ᴍᴏᴠɪᴇ ɴᴀᴍᴇ ➠ ᴄᴏᴘʏ ᴄᴏʀʀᴇᴄᴛ ɴᴀᴍᴇ ➠ ᴘᴀꜱᴛᴇ ᴛʜɪꜱ ɢʀᴏᴜᴘ\n\nᴇxᴀᴍᴘʟᴇ : ʟᴏᴋɪ S01 E01\n\n🚯 ᴅᴏɴᴛ ᴜꜱᴇ ➠ ':(!,./)\n\n© Tʜᴏᴍᴀs Sʜᴇʟʙʏ ™️", show_alert=True)   
                           
    elif query.data == "reason":
        await query.answer(script.SPELL_TXT, show_alert=True)        
        
    elif query.data =="set2":
   
        userid = query.from_user.id if query.from_user else None
        if not userid:
            return await query.reply(f"You are anonymous admin. Use /connect {query.message.chat.id} in PM")
        chat_type = query.message.chat.type

        if chat_type == enums.ChatType.PRIVATE:
            grpid = await active_connection(str(userid))
            if grpid is not None:
                grp_id = grpid
                try:
                    chat = await client.get_chat(grpid)
                    title = chat.title
                except:
                    await query.reply_text("Make sure I'm present in your group!!", quote=True)
                    return
            else:
                await query.reply_text("I'm not connected to any groups!", quote=True)
                return

        elif chat_type in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
            grp_id = query.message.chat.id
            title = query.message.chat.title

        else:
            return

        st = await client.get_chat_member(grp_id, userid)
        if (
                st.status != enums.ChatMemberStatus.ADMINISTRATOR
                and st.status != enums.ChatMemberStatus.OWNER
                and str(userid) not in ADMINS
        ):
            return
        settings = await get_settings(grp_id)
        if settings is not None:
            await query.answer('Sᴇɴᴛᴇᴅ ✅')
            buttons = [
                [
                    InlineKeyboardButton('Fɪʟᴛᴇʀ Bᴜᴛᴛᴏɴ',
                                         callback_data=f'setgs#button#{settings["button"]}#{str(grp_id)}'),
                    InlineKeyboardButton('Sɪɴɢʟᴇ' if settings["button"] else 'Dᴏᴜʙʟᴇ',
                                         callback_data=f'setgs#button#{settings["button"]}#{str(grp_id)}')
                ],
                
                
                [
                    InlineKeyboardButton('Iᴍᴅʙ', callback_data=f'setgs#imdb#{settings["imdb"]}#{str(grp_id)}'),
                    InlineKeyboardButton('Yᴇs' if settings["imdb"] else 'Nᴏ',
                                         callback_data=f'setgs#imdb#{settings["imdb"]}#{str(grp_id)}')
                ],
                [
                    InlineKeyboardButton('Sᴘᴇʟʟ Cʜᴇᴄᴋ',
                                         callback_data=f'setgs#spell_check#{settings["spell_check"]}#{str(grp_id)}'),
                    InlineKeyboardButton('Nᴇᴡ' if settings["spell_check"] else 'Dᴇғᴀᴜʟᴛ',
                                         callback_data=f'setgs#spell_check#{settings["spell_check"]}#{str(grp_id)}')
                ],
                
                [
                    InlineKeyboardButton('Cʟᴏsᴇ Sᴇᴛᴛɪɴɢs', callback_data='close_data')
                ]
            ]
            
            if settings["button"]:
                stats="Sɪɴɢʟᴇ"
            else:
                stats="Dᴏᴜʙʟᴇ"
            
            
            if settings["imdb"]:
                stats4="Yᴇs"
            else:
                stats4="Nᴏ"
            if settings["spell_check"]:
                stats5="Nᴇᴡ"
            else:
                stats5="Dᴇғᴀᴜʟᴛ"
     
            
            
            await client.send_message(
                chat_id=query.from_user.id,
                text=f"<b><u>Cᴜʀʀᴇɴᴛ sᴇᴛᴛɪɴɢs Fᴏʀ {title}</u></b>\n\nFɪʟᴛᴇʀ Bᴜᴛᴛᴏɴ : {stats}\nRᴇᴅɪᴇʀᴄᴛ Tᴏ : {stats2}\nAᴜᴛᴏ Fɪʟᴛᴇʀ : {stats3}\nIᴍᴅʙ : {stats4}\nSᴘᴇʟʟ Cʜᴇᴄᴋ : {stats5}\nWᴇʟᴄᴏᴍᴇ : {stats6}\n\n<b>Hᴇʏ Bᴜᴅᴅʏ Hᴇʀᴇ Yᴏᴜ Cᴀɴ Cʜᴀɴɢᴇ Sᴇᴛᴛɪɴɢs As Yᴏᴜʀ Wɪsʜ Bʏ Usɪɴɢ Bᴇʟᴡ Bᴜᴛᴛᴏɴs</b>",
                reply_markup=InlineKeyboardMarkup(buttons),
                parse_mode=enums.ParseMode.HTML
            )
            btn = [
                [
                    InlineKeyboardButton(
                        '📮 Gᴏ Tᴏ Tʜᴇ Cʜᴀᴛ 📮', url="t.me/CL_FILTER_BOT"
                    )
                ]
            ]
            await query.message.edit_text(
                text="<i><b>Sᴇᴛᴛɪɴɢs Mᴇɴᴜ Wᴀs Sᴇɴᴛ Iɴ Yᴏᴜʀ Pᴍ ✅</b></i>",
                reply_markup=InlineKeyboardMarkup(btn),
                parse_mode=enums.ParseMode.HTML
            )
              
    elif query.data.startswith("setgs"):
        ident, set_type, status, grp_id = query.data.split("#")
        grpid = await active_connection(str(query.from_user.id))
           
        if str(grp_id) != str(grpid):
            btn = [
                [
                    InlineKeyboardButton(
                        '❗Hᴏᴡ Tᴏ Cᴏɴɴᴇᴄᴛ A Cʜᴀᴛ❗', callback_data=f'connect'
                    )
                ]
            ]
            await query.message.edit_text(f"<u><b>Sᴏʀʀʏ {query.from_user.mention}</u>\n\nI Cᴀɴᴛ Oᴘᴇɴ Sᴇᴛᴛɪɴɢs Lᴏᴏᴋs Lɪᴋᴇ Iᴀᴍ Nᴏᴛ Cᴏɴɴᴇᴄᴛ Tᴏ {query.message.chat.title} 🤧\n\nNʙ : Iғ Yᴏᴜ Dɪᴅɴᴏᴛ Kɴᴏᴡ Hᴏᴡ Tᴏ Cᴏɴɴᴇᴄᴛ Cʟɪᴄᴋ Bᴇʟᴏᴡ Bᴜᴛᴛᴏɴ ❗", reply_markup=InlineKeyboardMarkup(btn), parse_mode=enums.ParseMode.HTML)
            return await query.answer()
        
        if status == "True":
            await save_group_settings(grpid, set_type, False)
        else:
            await save_group_settings(grpid, set_type, True)

        settings = await get_settings(grpid)

        if settings is not None:
            await query.answer('Cʜᴀɴɢɪɴɢ....')
            buttons = [
                [
                    InlineKeyboardButton('Fɪʟᴛᴇʀ Bᴜᴛᴛᴏɴ',
                                         callback_data=f'setgs#button#{settings["button"]}#{str(grp_id)}'),
                    InlineKeyboardButton('Sɪɴɢʟᴇ' if settings["button"] else 'Dᴏᴜʙʟᴇ',
                                         callback_data=f'setgs#button#{settings["button"]}#{str(grp_id)}')
                ],
                
                
                
                [
                    InlineKeyboardButton('Iᴍᴅʙ', callback_data=f'setgs#imdb#{settings["imdb"]}#{str(grp_id)}'),
                    InlineKeyboardButton('Yᴇs' if settings["imdb"] else 'Nᴏ',
                                         callback_data=f'setgs#imdb#{settings["imdb"]}#{str(grp_id)}')
                ],
                [
                    InlineKeyboardButton('Sᴘᴇʟʟ Cʜᴇᴄᴋ',
                                         callback_data=f'setgs#spell_check#{settings["spell_check"]}#{str(grp_id)}'),
                    InlineKeyboardButton('Nᴇᴡ' if settings["spell_check"] else 'Dᴇғᴀᴜʟᴛ',
                                         callback_data=f'setgs#spell_check#{settings["spell_check"]}#{str(grp_id)}')
                ],
                
                [
                    InlineKeyboardButton('Cʟᴏsᴇ Sᴇᴛᴛɪɴɢs', callback_data='close_data')
                ]
            ]
            reply_markup = InlineKeyboardMarkup(buttons)
            if settings["button"]:
                stats="Sɪɴɢʟᴇ"
            else:
                stats="Dᴏᴜʙʟᴇ"
           
            if settings["imdb"]:
                stats4="Yᴇs"
            else:
                stats4="Nᴏ"
            if settings["spell_check"]:
                stats5="Nᴇᴡ"
            else:
                stats5="Dᴇғᴀᴜʟᴛ"
    
    
            await query.message.edit_text(
                text=f"<b><u>Cᴜʀʀᴇɴᴛ sᴇᴛᴛɪɴɢs Fᴏʀ {query.message.chat.title}</u></b>\n\nFɪʟᴛᴇʀ Bᴜᴛᴛᴏɴ : {stats}\nRᴇᴅɪᴇʀᴄᴛ Tᴏ : {stats2}\nAᴜᴛᴏ Fɪʟᴛᴇʀ : {stats3}\nIᴍᴅʙ : {stats4}\nSᴘᴇʟʟ Cʜᴇᴄᴋ : {stats5}\nWᴇʟᴄᴏᴍᴇ : {stats6}\n\n<b>Hᴇʏ Bᴜᴅᴅʏ Hᴇʀᴇ Yᴏᴜ Cᴀɴ Cʜᴀɴɢᴇ Sᴇᴛᴛɪɴɢs As Yᴏᴜʀ Wɪsʜ Bʏ Usɪɴɢ Bᴇʟᴏᴡ Bᴜᴛᴛᴏɴs</b>",
                reply_markup=reply_markup,
                parse_mode=enums.ParseMode.HTML
            )
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
                    return await advantage_spell_check_1_(msg)
                else:
                    return await advantage_spell_check_2_(msg)
                    return
        else:
            return
    else:
        settings = await get_settings(msg.message.chat.id)
        message = msg.message.reply_to_message  # msg will be callback query
        mention = message.from_user.mention if message.from_user else "Aɴᴏᴜɴʏᴍᴜs"
        search, files, offset, total_results = spoll
    if settings["button"]:
        btn = [
            [
                InlineKeyboardButton(
                    text=f"⊹ {get_size(file.file_size)} ‣ {file.file_name}", callback_data=f'file#{file.file_id}#{msg.from_user.id if msg.from_user is not None else 0}'
                ),
            ]
            for file in files
        ]
    else:
        btn = [
            [
                InlineKeyboardButton(
                    text=f"{file.file_name}",
                    callback_data=f'file#{file.file_id}#{msg.from_user.id if msg.from_user is not None else 0}',
                ),
                InlineKeyboardButton(
                    text=f"{get_size(file.file_size)}",
                    callback_data=f'file#{file.file_id}#{msg.from_user.id if msg.from_user is not None else 0}',
                ),
            ]
            for file in files
        ]

    btn.insert(0, 
        [
            InlineKeyboardButton(f'Fɪʟᴇs: {total_results}', 'dupe'),
            InlineKeyboardButton(f'Mᴏᴠɪᴇ', 'dupe'),
            InlineKeyboardButton(f'Sᴇʀɪᴇꜱ', 'dupe')
        ]
    )
    

    if offset != "":
        key = f"{message.chat.id}-{message.id}"
        BUTTONS[key] = search
        req = message.from_user.id if message.from_user else 0
        btn.append(
            [InlineKeyboardButton("Pᴀɢᴇs", callback_data="pages"),
             InlineKeyboardButton(text=f"1 - {math.ceil(int(total_results) / 10)}", callback_data="pages"),
             InlineKeyboardButton(text="Nᴇxᴛ •", callback_data=f"next_{req}_{key}_{offset}")]
        )
        
    else:
        btn.append(
            [InlineKeyboardButton(text="Nᴏ Mᴏʀᴇ Fɪʟᴇs Fᴏᴜɴᴅ", callback_data="pages")]
        )
  
    
    imdb = await get_poster(search, file=(files[0]).file_name) if settings["imdb"] else None
    TEMPLATE = settings['template']
    if imdb:
        cap1 = TEMPLATE.format(
            query=search,
            title=imdb['title'],
            votes=imdb['votes'],
            aka=imdb["aka"],
            seasons=imdb["seasons"],
            box_office=imdb['box_office'],
            localized_title=imdb['localized_title'],
            kind=imdb['kind'],
            imdb_id=imdb["imdb_id"],
            cast=imdb["cast"],
            runtime=imdb["runtime"],
            countries=imdb["countries"],
            certificates=imdb["certificates"],
            languages=imdb["languages"],
       
       
       
       
       
       
       
       
       
       
     
     
     
     
     
     
     
