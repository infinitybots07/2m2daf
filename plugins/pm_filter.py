
import asyncio
import re
import ast
import random
import datetime
import pytz
from pyrogram.errors.exceptions.bad_request_400 import MediaEmpty, PhotoInvalidDimensions, WebpageMediaEmpty
from Script import script
import pyrogram
from database.connections_mdb import active_connection, all_connections, delete_connection, if_active, make_active, \
    make_inactive
from info import ADMINS, PICS_RT, AUTH_CHANNEL, AUTH_USERS, CUSTOM_FILE_CAPTION, AUTH_GROUPS, P_TTI_SHOW_OFF, IMDB, \
    SINGLE_BUTTON, SPELL_CHECK_REPLY, IMDB_TEMPLATE, DELETE_TIME, CH_FILTER, CH_LINK
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from pyrogram import Client, filters
from pyrogram.errors import FloodWait, UserIsBlocked, MessageNotModified, PeerIdInvalid
from utils import get_size, is_subscribed, get_poster, search_gagala, temp, get_settings, save_group_settings
from database.users_chats_db import db
from database.ia_filterdb import Media, get_file_details, get_search_results
from database.filters_mdb import (
    del_all,
    find_filter,
    get_filters,
)
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.ERROR)

BUTTONS = {}
SPELL_CHECK = {}


@Client.on_message(filters.group & filters.text & filters.incoming)
async def give_filter(client, message):
    k = await manual_filters(client, message)
    if k == False:
        await auto_filter(client, message)


@Client.on_callback_query(filters.regex(r"^next"))
async def next_page(bot, query):
    ident, req, key, offset = query.data.split("_")
    if int(req) not in [query.from_user.id, 0]:
        return await query.answer("⚠️ Hᴇʏ Bᴜᴅᴅʏ Sᴇᴀʀᴄʜ Yᴏᴜʀ Oᴡɴ 🤧", show_alert=True)
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
                    text=f"⊹ {get_size(file.file_size)} ‣ {file.file_name}", callback_data=f'files#{file.file_id}'
                ),
            ]
            for file in files
        ]
    else:
        btn = [
            [
                InlineKeyboardButton(
                    text=f"{file.file_name}", callback_data=f'files#{file.file_id}'
                ),
                InlineKeyboardButton(
                    text=f"{get_size(file.file_size)}",
                    callback_data=f'files_#{file.file_id}',
                ),
            ]
            for file in files
        ]

    btn.insert(0, 
        [
            InlineKeyboardButton(f'Fɪʟᴇs: {len(files)}', 'dupe'),
            InlineKeyboardButton(f'Mᴏᴠɪᴇ', 'movss'),
            InlineKeyboardButton(f'Sᴇʀɪᴇꜱ', 'moviis')
        ]
    )
   

    if 0 < offset <= 10:
        off_set = 0
    elif offset == 0:
        off_set = None
    else:
        off_set = offset - 10
    if n_offset == 0:
        btn.append(
            [InlineKeyboardButton("Pᴀɢᴇs", callback_data="pages"),
             InlineKeyboardButton(text=f"{round(int(offset)/10)+1} - {round(total/10)}", callback_data="pages"),
             InlineKeyboardButton("Bᴀᴄᴋ", callback_data=f"next_{req}_{key}_{off_set}")]
        )
       
    elif off_set is None:
        btn.append(
            [
                InlineKeyboardButton("Pᴀɢᴇs", callback_data="pages"),
                InlineKeyboardButton(text=f"{round(int(offset)/10)+1} - {round(total/10)}", callback_data="pages"),
                InlineKeyboardButton("Nᴇxᴛ", callback_data=f"next_{req}_{key}_{n_offset}")]
        )
        
    else:
        btn.append(
            [
                InlineKeyboardButton("Bᴀᴄᴋ", callback_data=f"next_{req}_{key}_{off_set}"),
                InlineKeyboardButton(text=f"{round(int(offset)/10)+1} - {round(total/10)}", callback_data="pages"),
                InlineKeyboardButton("Nᴇxᴛ", callback_data=f"next_{req}_{key}_{n_offset}")]
        )
        
    try:
        await query.edit_message_reply_markup(
            reply_markup=InlineKeyboardMarkup(btn)
        )
    except MessageNotModified:
        pass
    await query.answer(f'⍟ Pᴀɢᴇ Nᴏ : {round(int(offset) / 10) + 1} / {round(total/10)} ⍟ Tᴏᴛᴀʟ Rᴇsᴜʟᴛs : {len(files)}')


@Client.on_callback_query(filters.regex(r"^spolling"))
async def advantage_spoll_choker(bot, query):
    _, user, movie_ = query.data.split('#')
    if int(user) != 0 and query.from_user.id != int(user):
        return await query.answer("⚠️ Hᴇʏ Bᴜᴅᴅʏ Sᴇᴀʀᴄʜ Yᴏᴜʀ Oᴡɴ Dᴏɴ'ᴛ Rᴇǫᴜᴇsᴛ Oᴛʜᴇʀs 🤧", show_alert=True)
    if movie_ == "close_spellcheck":
        return await query.message.delete()
    movies = SPELL_CHECK.get(query.message.reply_to_message.message_id)
    if not movies:
        return await query.answer("Aʜʜ Bᴜᴛᴛᴏɴ Exᴘɪʀᴇᴅ 😒", show_alert=True)
    movie = movies[(int(movie_))]
    await query.answer('sᴇᴀʀᴄʜɪɴɢ ʏᴏᴜʀ ᴍᴏᴠɪᴇ')
    k = await manual_filters(bot, query.message, text=movie)
    if k == False:
        files, offset, total_results = await get_search_results(movie, offset=0, filter=True)
        if files:
            k = (movie, files, offset, total_results)
            await auto_filter(bot, query, k)
        else:
            k = await query.message.edit("<b>💌 ᴛʜɪs ᴍᴏᴠɪᴇ ɪs ɴᴏᴛ ʏᴇᴛ ʀᴇʟᴇᴀsᴇᴅ ᴏʀ ᴀᴅᴅᴇᴅ ᴛᴏ ᴍʏ ᴅᴀᴛᴀʙᴀsᴇ 💌</b>\n› <a href=https://t.me/CL_UPDATE><b>ɴᴇᴡ ᴜᴘᴅᴀᴛᴇs</b></a>", disable_web_page_preview=True)            
            await asyncio.sleep(14)
            await k.delete()


@Client.on_callback_query()
async def cb_handler(client: Client, query: CallbackQuery):
    if query.data == "close_data":
        await query.message.delete()
    elif query.data == "delallconfirm":
        userid = query.from_user.id
        chat_type = query.message.chat.type

        if chat_type == "private":
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
        elif chat_type in ["group", "supergroup"]:
            grp_id = query.message.chat.id
            title = query.message.chat.title

        else:
            return

        st = await client.get_chat_member(grp_id, userid)
        if (st.status == "creator") or (str(userid) in ADMINS):
            await del_all(query.message, grp_id, title)
        else:
            await query.answer("You need to be Group Owner or an Auth User to do that!", show_alert=True)
    elif query.data == "delallcancel":
        userid = query.from_user.id
        chat_type = query.message.chat.type

        if chat_type == "private":
            await query.message.reply_to_message.delete()
            await query.message.delete()

        elif chat_type in ["group", "supergroup"]:
            grp_id = query.message.chat.id
            st = await client.get_chat_member(grp_id, userid)
            if (st.status == "creator") or (str(userid) in ADMINS):
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
            parse_mode="md"
        )
        return await query.answer('Hᴀᴘᴘʏ Aʟʟᴇ Dᴀ')
    elif "connectcb" in query.data:
        await query.answer()

        group_id = query.data.split(":")[1]

        hr = await client.get_chat(int(group_id))
        
        title = hr.title

        user_id = query.from_user.id

        mkact = await make_active(str(user_id), str(group_id))

        if mkact:
            await query.message.edit_text(
                f"Cᴏɴɴᴇᴄᴛᴇᴅ ᴛᴏ **{title}**",
                parse_mode="md"
            )
        else:
            await query.message.edit_text('Some error occurred!!', parse_mode="md")
        return await query.answer('𝙿𝙻𝙴𝙰𝚂𝙴 𝚂𝙷𝙰𝚁𝙴 𝙰𝙽𝙳 𝚂𝚄𝙿𝙿𝙾𝚁𝚃')
    elif "disconnect" in query.data:
        await query.answer()

        group_id = query.data.split(":")[1]

        hr = await client.get_chat(int(group_id))

        title = hr.title
        user_id = query.from_user.id

        mkinact = await make_inactive(str(user_id))

        if mkinact:
            await query.message.edit_text(
                f"Disconnected from **{title}**",
                parse_mode="md"
            )
        else:
            await query.message.edit_text(
                f"Some error occurred!!",
                parse_mode="md"
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
                parse_mode="md"
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
                act = " - ACTIVE" if active else ""
                buttons.append(
                    [
                        InlineKeyboardButton(
                            text=f"{title}{act}", callback_data=f"groupcb:{groupid}:{act}"
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
        ident, file_id = query.data.split("#")
        files_ = await get_file_details(file_id)
        if not files_:
            return await query.answer('No such file exist.')
        files = files_[0]
        title = files.file_name
        size = get_size(files.file_size)
        f_caption = files.caption
        mention = {query.from_user.mention}
        settings = await get_settings(query.message.chat.id)
        if CUSTOM_FILE_CAPTION:
            try:
                f_caption = CUSTOM_FILE_CAPTION.format(file_name='' if title is None else title,
                                                       file_size='' if size is None else size,
                                                       file_caption='' if f_caption is None else f_caption)
                                                       
            except Exception as e:
                logger.exception(e)
            f_caption = f_caption
            size = size
            mention = mention
        if f_caption is None:
            f_caption = f"{files.file_name}"
            size = f"{files.file_size}"
            mention = f"{query.from_user.mention}"
        buttons = [[
            InlineKeyboardButton('➕ ᴀᴅᴅ ʙᴏᴛ ᴛᴏ ʏᴏᴜʀ ɢʀᴏᴜᴘ ➕', url=f'http://t.me/CL_FILTER_BOT?startgroup=true')
        ]]
        try:
            if AUTH_CHANNEL and not await is_subscribed(client, query):
                await query.answer(url=f"https://t.me/{temp.U_NAME}?start={ident}_{file_id}")
                return
            elif settings['botpm']:
                await query.answer(url=f"https://t.me/{temp.U_NAME}?start={ident}_{file_id}")
                return
            else:
                ms = await client.send_cached_media(
                    chat_id=CH_FILTER,
                    file_id=file_id,
                    caption=f'<b>ʜᴇʏ 👋 {query.from_user.mention} 😊</b>\n\n<b>📁 Fᴀᴍᴇ Nᴀᴍᴇ : <code>[CL] {title}</code></b>\n\n<b>⚙️ sɪᴢᴇ : {size}</b>\n\n<b><u>Nᴏᴛᴇ :</u></b>\n\n<b><i>⚠️ Tʜɪs Fɪʟᴇ EɪʟAᴜᴛɪ ᴅᴇʟᴇᴛᴇ Iɴ 10 Sᴏ Fᴏʀᴡᴀʀᴅ Tʜɪs Mᴇssᴀɢᴇʙ Tᴏ Sᴏᴍᴇᴡʜᴇʀᴇ Eʟsᴇ ᴀɴᴅ Fʀᴏᴍ Tʜᴇʀᴇ.. ⚠️</i></b>\n\n<b>🚀 Pᴏᴡᴇʀᴇᴅ Bʏ : {query.message.chat.title}</b>',
                    reply_markup = InlineKeyboardMarkup(buttons),
                    protect_content=True if ident == "filep" else False 
                )
                msg1 = await query.message.reply(
                f'<b> ʜᴇʏ 👋 {query.from_user.mention} </b>😍\n\n<b>📫 ʏᴏᴜʀ ғɪʟᴇ ɪs ʀᴇᴀᴅʏ 📥</b>\n\n'           
                f'<b>📂 Fɪʟᴇ Nᴀᴍᴇ</b> : <code>[CL] {title}</code>\n\n'              
                f'<b>⚙️ Fɪʟᴇ Sɪᴢᴇ</b> : <b>{size}</b>',
                True,
                'html',
                disable_web_page_preview=True,
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton("📥  Dᴏᴡɴʟᴏᴀᴅ Lɪɴᴋ  📥", url = ms.link)
                        ],
                        [
                            InlineKeyboardButton("⚠️ Cᴀɴɴᴏᴛ Aᴄᴄᴇss ❓ Cʟɪᴄᴋ Hᴇʀᴇ ⚠️", url = f"{CH_LINK}")
                        ]
                    ]
                )
            )
            await asyncio.sleep(300)
            await msg1.delete()            
            await ms.delete()
            del msg1, ms
        except Exception as e:
            logger.exception(e, exc_info=True)

    elif query.data.startswith("checksub"):
        if AUTH_CHANNEL and not await is_subscribed(client, query):
            await query.answer(f"Hey, {query.from_user.first_name}! I Like Your Smartness, But Don't Be Oversmart 😒",show_alert=True)
            return
        ident, file_id = query.data.split("#")
        files_ = await get_file_details(file_id)
        if not files_:
            return await query.answer(f'Hello, {query.from_user.first_name}! No such file exist. Send Request Again')
        files = files_[0]
        title = files.file_name
        size = get_size(files.file_size)
        f_caption = files.caption
        if CUSTOM_FILE_CAPTION:
            try:
                f_caption = CUSTOM_FILE_CAPTION.format(file_name='' if title is None else title,
                                                       file_size='' if size is None else size,
                                                       file_caption='' if f_caption is None else f_caption)
            except Exception as e:
                logger.exception(e)
                f_caption = f_caption
        if f_caption is None:
            f_caption = f"{title}"
        buttons = [[
            InlineKeyboardButton('➕ ᴀᴅᴅ ʙᴏᴛ ᴛᴏ ʏᴏᴜʀ ɢʀᴏᴜᴘ ➕', url=f'http://t.me/CL_FILTER_BOT?startgroup=true')
        ]] 
        await query.answer()
        ms = await client.send_cached_media(
            chat_id=query.from_user.id,
            file_id=file_id,
            caption=f_caption,
            reply_markup=InlineKeyboardMarkup(buttons),
            protect_content=True if ident == 'checksubp' else False
        )
    elif query.data == "pages":
        await query.answer()
    elif query.data == "start":
        m = datetime.datetime.now(pytz.timezone("Asia/Kolkata"))

        Time = m.hour
        
        if Time < 12:
            nihaal="ɢᴏᴏᴅ ᴍᴏʀɴɪɴɢ" 
        elif Time < 15:
            nihaal="ɢᴏᴏᴅ ᴀғᴛᴇʀɴᴏᴏɴ" 
        elif Time < 20:
            nihaal="ɢᴏᴏᴅ ᴇᴠᴇɴɪɴɢ"
        else:
            nihaal="ɢᴏᴏᴅ ɴɪɢʜᴛ"
        
        START_TXT = f"""
<b>{nihaal} {query.from_user.mention}  ʙᴜᴅᴅʏ
ᴍʏ ɴᴀᴍᴇ ɪꜱ  <a href=https://t.me/CL_FILTER_BOT><b>『 𝐓ʜᴏᴍᴀs 𝐒ʜᴇʟʙʏ 』</b></a>  ɪ ᴄᴀɴ ᴘʀᴏᴠɪᴅᴇ ʏᴏᴜ ᴍᴏᴠɪᴇꜱ ᴊᴜꜱᴛ ᴀᴅᴅ ᴍᴇ ᴛᴏ ʏᴏᴜʀ ɢʀᴏᴜᴘ ᴀɴᴅ ꜱᴇᴇ ᴍʏ ᴘᴏᴡᴇʀ 😈</b>
"""
        buttons = [[
      
            InlineKeyboardButton('Cʟɪᴄᴋ Hᴇʀᴇ Fᴏʀ Mᴏʀᴇ Bᴜᴛᴛᴏɴs', callback_data='start2')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(        
            text=START_TXT,
            reply_markup=reply_markup,
            disable_web_page_preview=True,
            parse_mode='html'
        )
      
    elif query.data == "start2":
        buttons = [[   
            InlineKeyboardButton('➕ Aᴅᴅ Mᴇ Tᴏ Yᴏᴜʀ Gʀᴏᴜᴘ ➕', url=f'http://t.me/CL_FILTER_BOT?startgroup=true')
        ],[
            InlineKeyboardButton('🍁 Oᴡɴᴇʀ', callback_data='owner'),
            InlineKeyboardButton('🌿 Gʀᴏᴜᴘ', url='https://t.me/cinema_lookam')
        ],[
            InlineKeyboardButton('❗ Hᴇʟᴘ', callback_data='help'),
            InlineKeyboardButton('🕵️‍♂️ Aʙᴏᴜᴛ', callback_data='about')
        ],[
            InlineKeyboardButton('👨‍🦯 ʙᴀᴄᴋ ᴛᴏ sᴛᴀʀᴛ 👨‍🦯', callback_data='start')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=script.START_TXT.format(query.from_user.mention, temp.U_NAME, temp.B_NAME),
            reply_markup=reply_markup,
            disable_web_page_preview=True,
            parse_mode='html'
        )
    elif query.data == "owner":
        buttons = [[
            InlineKeyboardButton('Tᴇʟᴇɢʀᴀᴍ', url='t.me/NL_MP4_BOT'),
            InlineKeyboardButton('Iɴsᴛᴀɢʀᴀᴍ', url='https://instagram.com')
        ],[
            InlineKeyboardButton('Bᴀᴄᴋ', callback_data='start2')
        ]]
        await query.message.edit_text(text='<u><b>Cᴏɴᴛᴀᴄᴛ Oᴡɴᴇʀ</u></b>\n\nHᴇʏ Bᴜᴅᴅʏ Hᴇʀᴇ Yᴏᴜ Cᴀɴ Cᴏɴᴛᴀᴄᴛ Mʏ Oᴡɴᴇʀ', reply_markup = InlineKeyboardMarkup(buttons), disable_web_page_preview=True, parse_mode='html')

    elif query.data == "help":
        buttons = [[
            InlineKeyboardButton('Fɪʟᴛᴇʀs', callback_data='filter'),
            InlineKeyboardButton('Cᴏɴɴᴇᴄᴛɪᴏɴ', callback_data='coct')
        ],[
            InlineKeyboardButton('Aᴅᴍɪɴ', callback_data='admin'),
            InlineKeyboardButton('Fɪʟᴇ Sᴛᴏʀᴇ', callback_data='fstore')
        ],[ 
            InlineKeyboardButton('Jsᴏɴ', callback_data='json'),
            InlineKeyboardButton('Sᴛᴀᴛᴜs', callback_data='stats')
        ],[
            InlineKeyboardButton('Bᴀᴄᴋ', callback_data='start2')
        ]]
        await query.message.edit_text(
            text=script.HELP_TXT.format(query.from_user.mention), 
            reply_markup = InlineKeyboardMarkup(buttons),
            disable_web_page_preview=True, 
            parse_mode='html'
        )

    elif query.data == "about":
        buttons = [[
            InlineKeyboardButton('Gʀᴏᴜᴘ', url='t.me/cinema_lookam'),
            InlineKeyboardButton('Sᴜᴘᴘᴏʀᴛ', url='t.me/NL_BOTxCHAT'),
            InlineKeyboardButton('Bᴀᴄᴋ', callback_data='start2')
        ]]
        await query.message.edit_text(text=script.ABOUT_TXT, reply_markup=InlineKeyboardMarkup(buttons), disable_web_page_preview=True, parse_mode='html')

    elif query.data == "filter":
        buttons = [[
            InlineKeyboardButton('Aᴜᴛᴏ Fɪʟᴛᴇʀ', callback_data='auto'),
            InlineKeyboardButton('Mᴀɴᴜᴀʟ Fɪʟᴛᴇʀ', callback_data="manual")
        ],[
            InlineKeyboardButton('Bᴀᴄᴋ', callback_data='help')
        ]]
        await query.message.edit_text(text="<b><u>Hᴇʟᴘ Fᴏʀ Fɪʟᴛᴇʀs</b></u>\n\nHᴇʏ Bᴜᴅᴅʏ Cʜᴏᴏsᴇ A Fɪʟᴛᴇʀ Tʏᴘᴇ", reply_markup = InlineKeyboardMarkup(buttons), disable_web_page_preview=True, parse_mode='html')
            
    elif query.data == "fstore":
        await query.answer("Page Does Not Exist :(")
        
    elif query.data == "coct":
        buttons = [[
            InlineKeyboardButton('Bᴀᴄᴋ', callback_data="help")
        ]]
        await query.message.edit_text(text=script.CONNECTION_TXT, reply_markup=InlineKeyboardMarkup(buttons), disable_web_page_preview=True, parse_mode='html')
        
    elif query.data == "admin":
        buttons = [[
            InlineKeyboardButton('Bᴀᴄᴋ', callback_data='help')
        ]]
        await query.message.edit_text(text=script.ADMIN_TXT, reply_markup = InlineKeyboardMarkup(buttons), parse_mode='html')
        
    elif query.data == "filestore":
        await query.answer("Page Does Not Exist")
     
    elif query.data == "json":
        buttons = [[
            InlineKeyboardButton('Bᴀᴄᴋ', callback_data='help')
        ]]
        await query.message.edit_text(text=script.JSON_TXT, reply_markup = InlineKeyboardMarkup(buttons), parse_mode='html')
        
    elif query.data == "auto":
        buttons = [[
            InlineKeyboardButton('Bᴀᴄᴋ', callback_data='filter')
        ]]
        await query.message.edit_text(text=script.AUTOFILTER_TXT, reply_markup = InlineKeyboardMarkup(buttons), parse_mode='html')
        
    elif query.data == "manual":
        buttons = [[
            InlineKeyboardButton('Bᴀᴄᴋ', callback_data='filter')
        ]]
        await query.message.edit_text(text=script.MANUALFILTER_TXT, reply_markup = InlineKeyboardMarkup(buttons), parse_mode='html')
        
    elif query.data == "stats":
        buttons = [[
            InlineKeyboardButton('ʙᴀᴄᴋ', callback_data='help'),
            InlineKeyboardButton('ʀᴇғʀᴇsʜ', callback_data='rfrsh')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        total = await Media.count_documents()
        users = await db.total_users_count()
        chats = await db.total_chat_count()
        monsize = await db.get_db_size()
        free = 536870912 - monsize
        monsize = get_size(monsize)
        free = get_size(free)
        await query.message.edit_text(
            text=script.STATUS_TXT.format(total, users, chats, monsize, free),
            reply_markup=reply_markup,
            parse_mode='html'
        )
    elif query.data == "rfrsh":
        await query.answer("ᴜᴘᴅᴀᴛɪɴɢ ᴍʏ ᴅʙ ᴅᴇᴛᴀɪʟs")
        buttons = [[
            InlineKeyboardButton('ʙᴀᴄᴋ', callback_data='help'),
            InlineKeyboardButton('ʀᴇғʀᴇsʜ', callback_data='rfrsh')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        total = await Media.count_documents()
        users = await db.total_users_count()
        chats = await db.total_chat_count()
        monsize = await db.get_db_size()
        free = 536870912 - monsize
        monsize = get_size(monsize)
        free = get_size(free)
        await query.message.edit_text(
            text=script.STATUS_TXT.format(total, users, chats, monsize, free),
            reply_markup=reply_markup,
            parse_mode='html'
        )
    elif query.data == "movss":
        await query.answer("⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯\nᴍᴏᴠɪᴇ ʀᴇǫᴜᴇꜱᴛ ꜰᴏʀᴍᴀᴛ\n⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯\n\nɢᴏ ᴛᴏ ɢᴏᴏɢʟᴇ ⪼ ᴛʏᴘᴇ ᴍᴏᴠɪᴇ ɴᴀᴍᴇ ⪼ ᴄᴏᴘʏ ᴄᴏʀʀᴇᴄᴛ ɴᴀᴍᴇ ⪼ ᴘᴀꜱᴛᴇ ᴛʜɪꜱ ɢʀᴏᴜᴘ\n\nᴇxᴀᴍᴘʟᴇ : ᴋɢꜰ ᴄʜᴀᴘᴛᴇʀ 2  2022\n\n✘ ᴅᴏɴᴛ ᴜꜱᴇ ➠ ':(!,./)\n\n© Tʜᴏᴍᴀs Sʜᴇʟʙʏ", show_alert=True)

    
    elif query.data == "moviis":  
        await query.message.answer("⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯\nꜱᴇʀɪᴇꜱ ʀᴇǫᴜᴇꜱᴛ ꜰᴏʀᴍᴀᴛ\n⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯\n\nɢᴏ ᴛᴏ ɢᴏᴏɢʟᴇ ⪼ ᴛʏᴘᴇ ᴍᴏᴠɪᴇ ɴᴀᴍᴇ ⪼ ᴄᴏᴘʏ ᴄᴏʀʀᴇᴄᴛ ɴᴀᴍᴇ ⪼ ᴘᴀꜱᴛᴇ ᴛʜɪꜱ ɢʀᴏᴜᴘ\n\nᴇxᴀᴍᴘʟᴇ : ʟᴏᴋɪ S01 E01\n\n✘ ᴅᴏɴᴛ ᴜꜱᴇ ➠ ':(!,./)\n\n© Tʜᴏᴍᴀs Sʜᴇʟʙʏ", show_alert=True)   
    
 
    elif query.data == "reason":
        await query.answer("✯ 𝖢𝗁𝖾𝖼𝗄 𝖮𝖳𝖳 𝖱𝖾𝗅𝖾𝖺𝗌𝖾 ᴏʀ 𝖢𝗈𝗋𝗋𝖾𝖼𝗍 𝖳𝗁𝖾 𝗌𝗉𝖾𝗅𝗅𝗂𝗇𝗀\n\n✯ 𝖣𝗈𝗇𝗍 𝖴𝗌𝖾 𝖲𝗒𝗆𝖻𝗈𝗅𝗌 𝖶𝗁𝗂𝗅𝖾 𝖱𝖾𝗊𝗎𝖾𝗌𝗍 (,:'?!* 𝖾𝗍𝖼..)\n\n✯ [𝖬𝗈𝗏𝗂𝖾 𝖭𝖺𝗆𝖾 ,𝖸𝖾𝖺𝗋 ,𝖫𝖺𝗇𝗀𝗎𝖺𝗀𝖾] 𝖠𝗌𝗄 𝖳𝗁𝗂𝗌 𝖶𝖺𝗒", show_alert=True)        
        
    elif query.data.startswith("setgs"):
        ident, set_type, status, grp_id = query.data.split("#")
        grpid = await active_connection(str(query.from_user.id))

        if str(grp_id) != str(grpid):
            await query.message.edit("⚠️ Sᴏʀʀʏ Bᴜᴅᴅʏ I Cᴀɴɴᴏᴛ Cʜᴀɴɢᴇ Sᴇᴛᴛɪɴɢs Pʟᴇᴀsᴇ Tʀʏ Iɴ Pᴍ ⚠️")
            return await query.answer('Hᴇʏ Nᴀᴜɢʜᴛʏ Bᴏʏ Tʜᴀᴛs Nᴏᴛ Fᴏʀ Yᴏᴜ')

        if status == "True":
            await save_group_settings(grpid, set_type, False)
        else:
            await save_group_settings(grpid, set_type, True)

        settings = await get_settings(grpid)

        if settings is not None:
            buttons = [
                [
                    InlineKeyboardButton('Fɪʟᴛᴇʀ Bᴜᴛᴛᴏɴ',
                                         callback_data=f'setgs#button#{settings["button"]}#{str(grp_id)}'),
                    InlineKeyboardButton('Sɪɴɢʟᴇ' if settings["button"] else 'Dᴏᴜʙʟᴇ',
                                         callback_data=f'setgs#button#{settings["button"]}#{str(grp_id)}')
                ],
                
                [
                    InlineKeyboardButton('Rᴇᴅɪʀᴇᴄᴛ Tᴏ', callback_data=f'setgs#botpm#{settings["botpm"]}#{str(grp_id)}'),
                    InlineKeyboardButton('Pᴍ' if settings["botpm"] else 'Cʜᴀᴛ',
                                         callback_data=f'setgs#botpm#{settings["botpm"]}#{str(grp_id)}')
                ],
                [
                    InlineKeyboardButton('Fɪʟᴇ Sᴇᴄᴜʀᴇ',
                                         callback_data=f'setgs#file_secure#{settings["file_secure"]}#{str(grp_id)}'),
                    InlineKeyboardButton('Yᴇs' if settings["file_secure"] else 'Nᴏ',
                                         callback_data=f'setgs#file_secure#{settings["file_secure"]}#{str(grp_id)}')
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
                    InlineKeyboardButton('Wᴇʟᴄᴏᴍᴇ', callback_data=f'setgs#welcome#{settings["welcome"]}#{str(grp_id)}'),
                    InlineKeyboardButton('Yᴇs' if settings["welcome"] else 'Nᴏ',
                                         callback_data=f'setgs#welcome#{settings["welcome"]}#{str(grp_id)}')
                ],
                [
                    InlineKeyboardButton('Cʟᴏsᴇ Sᴇᴛᴛɪɴɢs', callback_data='close_data')
                ]
            ]
            reply_markup = InlineKeyboardMarkup(buttons)
            await query.message.edit_reply_markup(reply_markup)
    
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
        search, files, offset, total_results = spoll
    pre = 'filep' if settings['file_secure'] else 'file'
    if settings["button"]:
        btn = [
            [
                InlineKeyboardButton(
                    text=f"⊹ {get_size(file.file_size)} ‣ {file.file_name}", callback_data=f'{pre}#{file.file_id}'
                ),
            ]
            for file in files
        ]
    else:
        btn = [
            [
                InlineKeyboardButton(
                    text=f"{file.file_name}",
                    callback_data=f'{pre}#{file.file_id}',
                ),
                InlineKeyboardButton(
                    text=f"{get_size(file.file_size)}",
                    callback_data=f'{pre}#{file.file_id}',
                ),
            ]
            for file in files
        ]

    btn.insert(0, 
        [
            InlineKeyboardButton(f'Fɪʟᴇs: {len(files)}', 'dupe'),
            InlineKeyboardButton(f'Mᴏᴠɪᴇ', 'movss'),
            InlineKeyboardButton(f'Sᴇʀɪᴇꜱ', 'moviis')
        ]
    )
    

    if offset != "":
        key = f"{message.chat.id}-{message.message_id}"
        BUTTONS[key] = search
        req = message.from_user.id if message.from_user else 0
        btn.append(
            [InlineKeyboardButton("Pᴀɢᴇs", callback_data="pages"),
             InlineKeyboardButton(text=f"1 - {round(int(total_results) / 10)}", callback_data="pages"),
             InlineKeyboardButton(text="Nᴇxᴛ", callback_data=f"next_{req}_{key}_{offset}")]
        )
        
    else:
        btn.append(
            [InlineKeyboardButton(text="sᴇʟᴇᴄᴛ ғɪʟᴇ ғʀᴏᴍ ᴀʙᴏᴠᴇ ʟɪɴᴋs", callback_data="pages")]
        )
        
    imdb = await get_poster(search, file=(files[0]).file_name) if settings["imdb"] else None
    TEMPLATE = settings['template']
    if imdb:
        cap = TEMPLATE.format(
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
            director=imdb["director"],
            writer=imdb["writer"],
            producer=imdb["producer"],
            composer=imdb["composer"],
            cinematographer=imdb["cinematographer"],
            music_team=imdb["music_team"],
            distributors=imdb["distributors"],
            release_date=imdb['release_date'],
            year=imdb['year'],
            genres=imdb['genres'],
            poster=imdb['poster'],
            plot=imdb['plot'],
            rating=imdb['rating'],
            url=imdb['url'],
            **locals()
        )
    else:
        cap = f"<b><i>🎬 Mᴏᴠɪᴇ ɴᴀᴍᴇ : {search}\n👩🏻‍💻 Rᴇǫᴜᴇsᴛᴇᴅ ʙʏ : {message.from_user.mention}\n🚀 Gʀᴏᴜᴘ : {message.chat.title}</i></b>"
    if imdb and imdb.get('poster'):
        try:
            fmsg = await message.reply_photo(photo=imdb.get('poster'), caption=cap[:1024],
                                      reply_markup=InlineKeyboardMarkup(btn))
        except (MediaEmpty, PhotoInvalidDimensions, WebpageMediaEmpty):
            pic = imdb.get('poster')
            poster = pic.replace('.jpg', "._V1_UX360.jpg")
            fmsg = await message.reply_photo(photo=poster, caption=cap[:1024], reply_markup=InlineKeyboardMarkup(btn))
        except Exception as e:
            logger.exception(e)
            fmsg = await message.reply_text(cap, reply_markup=InlineKeyboardMarkup(btn))
    else:
        fmsg = await message.reply_text(cap, reply_markup=InlineKeyboardMarkup(btn))
    
    await asyncio.sleep(DELETE_TIME)
    await message.delete()
    await fmsg.delete()
  
    if spoll:
        await msg.message.delete()
        
##-------------------------------------[ 1st Spell Check Message ]-------------------------------------------##

async def advantage_spell_check_1_(msg):
    search = msg.text
    query = re.sub(
        r"\b(pl(i|e)*?(s|z+|ease|se|ese|(e+)s(e)?)|((send|snd|giv(e)?|gib)(\sme)?)|movie(s)?|new|latest|br((o|u)h?)*|^h(e|a)?(l)*(o)*|mal(ayalam)?|t(h)?amil|file|that|find|und(o)*|kit(t(i|y)?)?o(w)?|thar(u)?(o)*w?|kittum(o)*|aya(k)*(um(o)*)?|full\smovie|any(one)|with\ssubtitle(s)?)",
        "", msg.text, flags=re.IGNORECASE)  # plis contribute some common words
    query = query.strip() + " movie"
    g_s = await search_gagala(query)
    g_s += await search_gagala(msg.text)
    gs_parsed = []
    if not g_s:
        buttons = [[
            InlineKeyboardButton('🍁 Rᴇᴀsᴏɴ', callback_data="reason"),
        ]]
        a = await msg.reply(f"<b><u>Hᴇʟʟᴏ Bᴜᴅᴅʏ</b></u>\n\nI Cᴏᴜʟᴅ Nᴏᴛ Fɪɴᴅ Aɴʏᴛʜɪɴɢ Rᴇʟᴀᴛᴇᴅ Tᴏ Tʜᴀᴛ\nPʟᴇᴀsᴇ Cʜᴇᴄᴋ Yᴏᴜʀ Sᴘᴇʟʟɪɴɢ 🤧", reply_markup = InlineKeyboardMarkup(buttons))
        await asyncio.sleep(100)
        await msg.delete()
        await a.delete()
        return
    regex = re.compile(r".*(imdb|wikipedia).*", re.IGNORECASE)  # look for imdb / wiki results
    gs = list(filter(regex.match, g_s))
    gs_parsed = [re.sub(
        r'\b(\-([a-zA-Z-\s])\-\simdb|(\-\s)?imdb|(\-\s)?wikipedia|\(|\)|\-|reviews|full|all|episode(s)?|film|movie|series)',
        '', i, flags=re.IGNORECASE) for i in gs]
    if not gs_parsed:
        reg = re.compile(r"watch(\s[a-zA-Z0-9_\s\-\(\)]*)*\|.*",
                         re.IGNORECASE)  # match something like Watch Niram | Amazon Prime
        for mv in g_s:
            match = reg.match(mv)
            if match:
                gs_parsed.append(match.group(1))
    user = msg.from_user.id if msg.from_user else 0
    movielist = []
    gs_parsed = list(dict.fromkeys(gs_parsed))  # removing duplicates https://stackoverflow.com/a/7961425
    if len(gs_parsed) > 3:
        gs_parsed = gs_parsed[:3]
    if gs_parsed:
        for mov in gs_parsed:
            imdb_s = await get_poster(mov.strip(), bulk=True)  # searching each keyword in imdb
            if imdb_s:
                movielist += [movie.get('title') for movie in imdb_s]
    movielist += [(re.sub(r'(\-|\(|\)|_)', '', i, flags=re.IGNORECASE)).strip() for i in gs_parsed]
    movielist = list(dict.fromkeys(movielist))  # removing duplicates
    if not movielist:
        reply = search.replace(" ", "+")
        buttons = [[
            InlineKeyboardButton('🍁 Rᴇᴀsᴏɴ', "reason"),
            InlineKeyboardButton('🔎 Sᴇᴀʀᴄʜ', url=f'https://google.com/search?q={reply}')
        ]]
        a2 = await msg.reply(f"<b><u>Hᴇʟʟᴏ {msg.from_user.mention}</b></u>\n\nI Cᴏᴜʟᴅ Nᴏᴛ Fɪɴᴅ Aɴʏᴛʜɪɴɢ Rᴇʟᴀᴛᴇᴅ Tᴏ Tʜᴀᴛ\nPʟᴇᴀsᴇ Cʜᴇᴄᴋ Yᴏᴜʀ Sᴘᴇʟʟɪɴɢ 🤧", reply_markup = InlineKeyboardMarkup(buttons))
        await asyncio.sleep(100)
        await msg.delete()
        await a2.delete()
        return
    SPELL_CHECK[msg.message_id] = movielist
    reply = search.replace(" ", "+")
    reply_markup = InlineKeyboardMarkup([[
     InlineKeyboardButton("🧿 Iᴍᴅʙ Iɴғᴏ", url=f"https://imdb.com/find?q={reply}")
     ],[
     InlineKeyboardButton("😌 Rᴇᴀsᴏɴ", callback_data="reason"),
     InlineKeyboardButton("🎭 Gᴏᴏɢʟᴇ", url=f"https://google.com/search?q={reply}")
     ]]
    )    
    imdb=await get_poster(search)
    if imdb and imdb.get('poster'):
        ms = await msg.reply_photo(
            photo=imdb.get('poster'), 
            caption=script.IMDB_MOVIE_2.format(query=search, title=imdb.get('title'), rating=imdb.get('rating'), genres=imdb.get('genres'), year=imdb.get('year'), runtime=imdb.get('runtime'), language=imdb.get('languages'), group=msg.chat.title, url="https://t.me/CL_UPDATE", short=imdb['plot']), 
            reply_markup=reply_markup
        ) 
        await asyncio.sleep(259200)
        await msg.delete()
        await ms.delete()
    if not imdb:
    imdb=await get_poster(search)
        ni = await msg.reply_photo(photo="https://telegra.ph/file/90049c7aa5b86b101a8d7.jpg", caption=script.IMDB_MOVIE_2.format(query=search, title=imdb.get('title'), rating=imdb.get('rating'), genres=imdb.get('genres'), year=imdb.get('year'), runtime=imdb.get('runtime'), language=imdb.get('languages'), group=msg.chat.title, url="https://t.me/CL_UPDATE", short=imdb['plot']), reply_markup=reply_markup)
        await asyncio.sleep(259200)
        await msg.delete()
        await ni.delete()
    else:
        buttons = [[
            InlineKeyboardButton('🍁 Rᴇᴀsᴏɴ', "reason"),
            InlineKeyboardButton('🔎 Sᴇᴀʀᴄʜ', url=f'https://google.com/search?q={reply}')
        ]]
        a3 = await msg.reply(f"<b><u>Hᴇʟʟᴏ {msg.from_user.mention}</b></u>\n\nI Cᴏᴜʟᴅ Nᴏᴛ Fɪɴᴅ Aɴʏᴛʜɪɴɢ Rᴇʟᴀᴛᴇᴅ Tᴏ Tʜᴀᴛ\nPʟᴇᴀsᴇ Cʜᴇᴄᴋ Yᴏᴜʀ Sᴘᴇʟʟɪɴɢ 🤧", reply_markup = InlineKeyboardMarkup(buttons))
        await asyncio.sleep(100)
        await msg.delete()
        await a3.delete()
        return
    
##--------------------------------[ 2nd Spell Check Message ]-------------------------------##

async def advantage_spell_check_2_(msg):
    query = re.sub(
        r"\b(pl(i|e)*?(s|z+|ease|se|ese|(e+)s(e)?)|((send|snd|giv(e)?|gib)(\sme)?)|movie(s)?|new|latest|br((o|u)h?)*|^h(e|a)?(l)*(o)*|mal(ayalam)?|t(h)?amil|file|that|find|und(o)*|kit(t(i|y)?)?o(w)?|thar(u)?(o)*w?|kittum(o)*|aya(k)*(um(o)*)?|full\smovie|any(one)|with\ssubtitle(s)?)",
        "", msg.text, flags=re.IGNORECASE)  # plis contribute some common words
    query = query.strip() + " movie"
    g_s = await search_gagala(query)
    g_s += await search_gagala(msg.text)
    gs_parsed = []
    if not g_s:
        k = await msg.reply("<b>I couldn't find any movie in that name.</b>\n› <a href=https://t.me/MWUpdatez><b>ᴍᴡ ᴜᴘᴅᴀᴛᴇᴢ</b></a>")
        await asyncio.sleep(8)
        await k.delete()
        return
    regex = re.compile(r".*(imdb|wikipedia).*", re.IGNORECASE)  # look for imdb / wiki results
    gs = list(filter(regex.match, g_s))
    gs_parsed = [re.sub(
        r'\b(\-([a-zA-Z-\s])\-\simdb|(\-\s)?imdb|(\-\s)?wikipedia|\(|\)|\-|reviews|full|all|episode(s)?|film|movie|series)',
        '', i, flags=re.IGNORECASE) for i in gs]
    if not gs_parsed:
        reg = re.compile(r"watch(\s[a-zA-Z0-9_\s\-\(\)]*)*\|.*",
                         re.IGNORECASE)  # match something like Watch Niram | Amazon Prime
        for mv in g_s:
            match = reg.match(mv)
            if match:
                gs_parsed.append(match.group(1))
    user = msg.from_user.id if msg.from_user else 0
    movielist = []
    gs_parsed = list(dict.fromkeys(gs_parsed))  # removing duplicates https://stackoverflow.com/a/7961425
    if len(gs_parsed) > 3:
        gs_parsed = gs_parsed[:3]
    if gs_parsed:
        for mov in gs_parsed:
            imdb_s = await get_poster(mov.strip(), bulk=True)  # searching each keyword in imdb
            if imdb_s:
                movielist += [movie.get('title') for movie in imdb_s]
    movielist += [(re.sub(r'(\-|\(|\)|_)', '', i, flags=re.IGNORECASE)).strip() for i in gs_parsed]
    movielist = list(dict.fromkeys(movielist))  # removing duplicates
    if not movielist:
        k = await msg.reply("I couldn't find anything related to that. Check your spelling")
        await asyncio.sleep(8)
        await k.delete()
        return
    SPELL_CHECK[msg.message_id] = movielist
    btn = [[
        InlineKeyboardButton(
            text=movie.strip(),
            callback_data=f"spolling#{user}#{k}",
        )
    ] for k, movie in enumerate(movielist)]
    btn.append([InlineKeyboardButton(text="ᴄʟᴏsᴇ", callback_data=f'spolling#{user}#close_spellcheck')])
    s = await msg.reply("<b>ɪ ᴄᴏᴜʟᴅɴ'ᴛ ғɪɴᴅ ᴀɴʏᴛʜɪɴɢ ʀᴇʟᴀᴛᴇᴅ ᴛᴏ ᴛʜᴀᴛ\n\nᴄʜᴇᴄᴋ ᴀɴᴅ sᴇʟᴇᴄᴛ ᴛʜᴇ ᴍᴏᴠɪᴇ ғʀᴏᴍ ᴛʜᴇ ɢɪᴠᴇɴ ʟɪsᴛ</b>",
                        reply_markup=InlineKeyboardMarkup(btn), disable_web_page_preview=True)
    await asyncio.sleep(30)
    await s.delete()

##-------------------------------------[ The End ]-------------------------------------------##

async def manual_filters(client, message, text=False):
    group_id = message.chat.id
    name = text or message.text
    reply_id = message.reply_to_message.message_id if message.reply_to_message else message.message_id
    keywords = await get_filters(group_id)
    for keyword in reversed(sorted(keywords, key=len)):
        pattern = r"( |^|[^\w])" + re.escape(keyword) + r"( |$|[^\w])"
        if re.search(pattern, name, flags=re.IGNORECASE):
            reply_text, btn, alert, fileid = await find_filter(group_id, keyword)

            if reply_text:
                reply_text = reply_text.replace("\\n", "\n").replace("\\t", "\t")

            if btn is not None:
                try:
                    if fileid == "None":
                        if btn == "[]":
                            await client.send_message(group_id, reply_text, disable_web_page_preview=True)
                        else:
                            button = eval(btn)
                            await client.send_message(
                                group_id,
                                reply_text,
                                disable_web_page_preview=True,
                                reply_markup=InlineKeyboardMarkup(button),
                                reply_to_message_id=reply_id
                            )
                    elif btn == "[]":
                        await client.send_cached_media(
                            group_id,
                            fileid,
                            caption=reply_text or "",
                            reply_to_message_id=reply_id
                        )
                    else:
                        button = eval(btn)
                        await message.reply_cached_media(
                            fileid,
                            caption=reply_text or "",
                            reply_markup=InlineKeyboardMarkup(button),
                            reply_to_message_id=reply_id
                        )
                except Exception as e:
                    logger.exception(e)
                break
    else:
        return False
