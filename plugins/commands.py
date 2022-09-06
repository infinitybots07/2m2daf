import os
import logging
import random
import asyncio
import datetime
import pytz
from Script import script
from pyrogram import Client, filters
from pyrogram.errors import ChatAdminRequired, FloodWait
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from database.ia_filterdb import Media, get_file_details, unpack_new_file_id
from database.users_chats_db import db
from info import CHANNELS, ADMINS, AUTH_CHANNEL, LOG_CHANNEL, PICS, BATCH_FILE_CAPTION, CUSTOM_FILE_CAPTION, PROTECT_CONTENT
from utils import get_settings, get_size, is_subscribed, save_group_settings, temp
from database.connections_mdb import active_connection
import re
import json
import base64
logger = logging.getLogger(__name__)

BATCH_FILES = {}

@Client.on_message(filters.command("start"))
async def start(client, message):
    if message.chat.type in ['group', 'supergroup']:
        await message.reply_photo(photo=random.choice(PICS))
        buttons = [[
      
            InlineKeyboardButton('➕ Aᴅᴅ Bᴏᴛ Tᴏ Yᴏᴜʀ Gʀᴏᴜᴘ ➕', url='http://t.me/CL_FILTER_BOT?startgroup=true')
        ]]     
        reply_markup = InlineKeyboardMarkup(buttons)
        await client.send_message(chat_id=message.chat.id, text=script.START_TXT.format(message.from_user.mention if message.from_user else message.chat.title, temp.U_NAME, temp.B_NAME), reply_markup=reply_markup)
        await asyncio.sleep(2) # 😢 https://github.com/Aadhi000/Ajax-Extra-Features/blob/master/plugins/p_ttishow.py#L17 😬 wait a bit, before checking.
        if not await db.get_chat(message.chat.id):
            total=await client.get_chat_members_count(message.chat.id)
            await client.send_message(LOG_CHANNEL, script.LOG_TEXT_G.format(message.chat.title, message.chat.id, total, "Unknown"))       
            await db.add_chat(message.chat.id, message.chat.title)
        return 
    if not await db.is_user_exist(message.from_user.id):
        await db.add_user(message.from_user.id, message.from_user.first_name)
        await client.send_message(LOG_CHANNEL, script.LOG_TEXT_P.format(message.from_user.id, message.from_user.mention))
    if len(message.command) != 2:
        await message.reply_photo(photo=random.choice(PICS))
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
<b>{nihaal} {message.from_user.mention}  ʙᴜᴅᴅʏ
ᴍʏ ɴᴀᴍᴇ ɪꜱ  <a href=https://t.me/CL_FILTER_BOT><b>『 𝐓ʜᴏᴍᴀs 𝐒ʜᴇʟʙʏ 』</b></a>  ɪ ᴄᴀɴ ᴘʀᴏᴠɪᴅᴇ ʏᴏᴜ ᴍᴏᴠɪᴇꜱ ᴊᴜꜱᴛ ᴀᴅᴅ ᴍᴇ ᴛᴏ ʏᴏᴜʀ ɢʀᴏᴜᴘ ᴀɴᴅ ꜱᴇᴇ ᴍʏ ᴘᴏᴡᴇʀ 😈</b>
"""
        buttons = [[
      
            InlineKeyboardButton('Cʟɪᴄᴋ ʜᴇʀᴇ Fᴏʀ Mᴏʀᴇ ʙᴜᴛᴛᴏɴ', callback_data='start2')
        ]]     
        reply_markup = InlineKeyboardMarkup(buttons)        
        await client.sent_message(
            chat_id=message.from_user.id,
            text=START_TXT,
            disable_web_page_preview=True,
            reply_markup=reply_markup,
            parse_mode='html'
        )        
        return
    if AUTH_CHANNEL and not await is_subscribed(client, message):
        try:
            invite_link = await client.create_chat_invite_link(int(AUTH_CHANNEL))
        except ChatAdminRequired:
            logger.error("Make sure Bot is admin in Forcesub channel")
            return
        btn = [
            [
                InlineKeyboardButton(
                    "📧 ᴊᴏɪɴ ᴄʜᴀɴɴᴇʟ 📧", url=invite_link.invite_link
                )
            ]
        ]
        await client.send_message(
            chat_id=message.from_user.id,
            text="**ᴊᴏɪɴ ᴛʜᴇ ᴜᴘᴅᴀᴛᴇs ᴄʜᴀɴɴᴇʟ ᴛʜᴇɴ ɢᴏ ʙᴀᴄᴋ ᴀɴᴅ ᴄʟɪᴄᴋ ᴛʜᴇ ʟɪɴᴋ ᴀɢᴀɪɴ ғᴏʀ ғɪʟᴇs.!**",
            reply_markup=InlineKeyboardMarkup(btn),
            parse_mode="markdown"
            )
 
        return
    if len(message.command) ==2 and message.command[1] in ["subscribe", "error", "okay", "help"]:
        await message.reply_photo(photo=random.choice(PICS))
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
<b>{nihaal} {message.from_user.mention}  ʙᴜᴅᴅʏ
ᴍʏ ɴᴀᴍᴇ ɪꜱ  <a href=https://t.me/CL_FILTER_BOT><b>『 𝐓ʜᴏᴍᴀs 𝐒ʜᴇʟʙʏ 』</b></a>  ɪ ᴄᴀɴ ᴘʀᴏᴠɪᴅᴇ ʏᴏᴜ ᴍᴏᴠɪᴇꜱ ᴊᴜꜱᴛ ᴀᴅᴅ ᴍᴇ ᴛᴏ ʏᴏᴜʀ ɢʀᴏᴜᴘ ᴀɴᴅ ꜱᴇᴇ ᴍʏ ᴘᴏᴡᴇʀ 😈</b>
"""
        buttons = [[
            InlineKeyboardButton('Cʟɪᴄᴋ ʜᴇʀᴇ Fᴏʀ Mᴏʀᴇ ʙᴜᴛᴛᴏɴ', callback_data='start2')
        ]]     
        reply_markup = InlineKeyboardMarkup(buttons)        
        await client.sent_message(
            chat_id=message.from_user.id,
            text=START_TXT,
            disable_web_page_preview=True,
            reply_markup=reply_markup,
            parse_mode='html'
        )
        return
    data = message.command[1]
    try:
        pre, file_id = data.split('_', 1)
    except:
        file_id = data
        pre = ""
    if data.split("-", 1)[0] == "BATCH":
        sts = await message.reply("ᴀᴄᴄᴇssɪɴɢ ғɪʟᴇs")
        file_id = data.split("-", 1)[1]
        msgs = BATCH_FILES.get(file_id)
        if not msgs:
            file = await client.download_media(file_id)
            try: 
                with open(file) as file_data:
                    msgs=json.loads(file_data.read())
            except:
                await sts.edit("FAILED")
                return await client.send_message(LOG_CHANNEL, "UNABLE TO OPEN FILE.")
            os.remove(file)
            BATCH_FILES[file_id] = msgs
        for msg in msgs:
            title = msg.get("title")
            size=get_size(int(msg.get("size", 0)))
            f_caption=msg.get("caption", "")
            if BATCH_FILE_CAPTION:
                try:
                    f_caption=BATCH_FILE_CAPTION.format(file_name= '' if title is None else title, file_size='' if size is None else size, file_caption='' if f_caption is None else f_caption)
                except Exception as e:
                    logger.exception(e)
                    f_caption=f_caption
            if f_caption is None:
                f_caption = f"{title}"
            try:
                await client.send_cached_media(
                    chat_id=message.from_user.id,
                    file_id=msg.get("file_id"),
                    caption=f_caption,
                    protect_content=msg.get('protect', False),
                    )
                
            except FloodWait as e:
                await asyncio.sleep(e.x)
                logger.warning(f"Floodwait of {e.x} sec.")
                await client.send_cached_media(
                    chat_id=message.from_user.id,
                    file_id=msg.get("file_id"),
                    caption=f_caption,
                    protect_content=msg.get('protect', False),
                    )
            except Exception as e:
                logger.warning(e, exc_info=True)
                continue
            await asyncio.sleep(1) 
        await sts.delete()
        return
    elif data.split("-", 1)[0] == "DSTORE":
        sts = await message.reply("ᴀᴄᴄᴇssɪɴɢ ғɪʟᴇs")
        b_string = data.split("-", 1)[1]
        decoded = (base64.urlsafe_b64decode(b_string + "=" * (-len(b_string) % 4))).decode("ascii")
        try:
            f_msg_id, l_msg_id, f_chat_id, protect = decoded.split("_", 3)
        except:
            f_msg_id, l_msg_id, f_chat_id = decoded.split("_", 2)
            protect = "/pbatch" if PROTECT_CONTENT else "batch"
        diff = int(l_msg_id) - int(f_msg_id)
        async for msg in client.iter_messages(int(f_chat_id), int(l_msg_id), int(f_msg_id)):
            if msg.media:
                media = getattr(msg, msg.media)
                if BATCH_FILE_CAPTION:
                    try:
                        f_caption=BATCH_FILE_CAPTION.format(file_name=getattr(media, 'file_name', ''), file_size=getattr(media, 'file_size', ''), file_caption=getattr(msg, 'caption', ''))
                    except Exception as e:
                        logger.exception(e)
                        f_caption = getattr(msg, 'caption', '')
                else:
                    media = getattr(msg, msg.media.value)
                    file_name = getattr(media, 'file_name', '')
                    f_caption = getattr(msg, 'caption', file_name)
                try:
                    await msg.copy(message.chat.id, caption=f_caption, protect_content=True if protect == "/pbatch" else False)
                except FloodWait as e:
                    await asyncio.sleep(e.x)
                    await msg.copy(message.chat.id, caption=f_caption, protect_content=True if protect == "/pbatch" else False)
                except Exception as e:
                    logger.exception(e)
                    continue
            elif msg.empty:
                continue
            else:
                try:
                    await msg.copy(message.chat.id, protect_content=True if protect == "/pbatch" else False)
                except FloodWait as e:
                    await asyncio.sleep(e.x)
                    await msg.copy(message.chat.id, protect_content=True if protect == "/pbatch" else False)
                except Exception as e:
                    logger.exception(e)
                    continue
            await asyncio.sleep(1) 
        return await sts.delete()
        

    files_ = await get_file_details(file_id)           
    if not files_:
        pre, file_id = ((base64.urlsafe_b64decode(data + "=" * (-len(data) % 4))).decode("ascii")).split("_", 1)
        try:
            msg = await client.send_cached_media(
                chat_id=message.from_user.id,
                file_id=file_id,
                protect_content=True if pre == 'filep' else False,
                )
            filetype = msg.media
            file = getattr(msg, filetype)
            title = file.file_name
            size=get_size(file.file_size)
            f_caption = f"<code>{title}</code>"
            if CUSTOM_FILE_CAPTION:
                try:
                    f_caption=CUSTOM_FILE_CAPTION.format(file_name= '' if title is None else title, file_size='' if size is None else size, file_caption='')
                except:
                    return
            await msg.edit_caption(f_caption)
            return
        except:
            pass
        return await message.reply('No such file exist...Request Again')
    files = files_[0]
    title = files.file_name
    size=get_size(files.file_size)
    f_caption=files.caption
    if CUSTOM_FILE_CAPTION:
        try:
            f_caption=CUSTOM_FILE_CAPTION.format(file_name= '' if title is None else title, file_size='' if size is None else size, file_caption='' if f_caption is None else f_caption)
        except Exception as e:
            logger.exception(e)
            f_caption=f_caption
    if f_caption is None:
        f_caption = f"{files.file_name}"
    await client.send_cached_media(
        chat_id=message.from_user.id,
        file_id=file_id,
        caption=f_caption,
        protect_content=True if pre == 'filep' else False,
        )
                    

@Client.on_message(filters.command('channel') & filters.user(ADMINS))
async def channel_info(bot, message):
           
    """Send basic information of channel"""
    if isinstance(CHANNELS, (int, str)):
        channels = [CHANNELS]
    elif isinstance(CHANNELS, list):
        channels = CHANNELS
    else:
        raise ValueError("Unexpected type of CHANNELS")

    text = '📑 **Indexed channels/groups**\n'
    for channel in channels:
        chat = await bot.get_chat(channel)
        if chat.username:
            text += '\n@' + chat.username
        else:
            text += '\n' + chat.title or chat.first_name

    text += f'\n\n**Total:** {len(CHANNELS)}'

    if len(text) < 4096:
        await message.reply(text)
    else:
        file = 'Indexed channels.txt'
        with open(file, 'w') as f:
            f.write(text)
        await message.reply_document(file)
        os.remove(file)


@Client.on_message(filters.command('logs') & filters.user(ADMINS))
async def log_file(bot, message):
    """Send log file"""
    try:
        await message.reply_document('TelegramBot.log')
    except Exception as e:
        await message.reply(str(e))

@Client.on_message(filters.command('delete') & filters.user(ADMINS))
async def delete(bot, message):
    """Delete file from database"""
    reply = message.reply_to_message
    if reply and reply.media:
        msg = await message.reply("ᴅᴇʟᴇᴛɪɴɢ..", quote=True)
    else:
        await message.reply('Reply to file with /delete which you want to delete', quote=True)
        return

    for file_type in ("document", "video", "audio"):
        media = getattr(reply, file_type, None)
        if media is not None:
            break
    else:
        await msg.edit('This is not supported file format')
        return
    
    file_id, file_ref = unpack_new_file_id(media.file_id)

    result = await Media.collection.delete_one({
        '_id': file_id,
    })
    if result.deleted_count:
        await msg.edit('ғɪʟᴇ sᴜᴄᴄᴇssғᴜʟʟʏ ᴅᴇʟᴇᴛᴇᴅ')
    else:
        file_name = re.sub(r"(_|\-|\.|\+)", " ", str(media.file_name))
        result = await Media.collection.delete_many({
            'file_name': file_name,
            'file_size': media.file_size,
            'mime_type': media.mime_type
            })
        if result.deleted_count:
            await msg.edit('ғɪʟᴇ sᴜᴄᴄᴇssғᴜʟʟʏ ᴅᴇʟᴇᴛᴇᴅ')
        else:
            # files indexed before https://github.com/EvamariaTG/EvaMaria/commit/f3d2a1bcb155faf44178e5d7a685a1b533e714bf#diff-86b613edf1748372103e94cacff3b578b36b698ef9c16817bb98fe9ef22fb669R39 
            # have original file name.
            result = await Media.collection.delete_many({
                'file_name': media.file_name,
                'file_size': media.file_size,
                'mime_type': media.mime_type
            })
            if result.deleted_count:
                await msg.edit('ғɪʟᴇ sᴜᴄᴄᴇssғᴜʟʟʏ ᴅᴇʟᴇᴛᴇᴅ')
            else:
                await msg.edit('File not found in database')


@Client.on_message(filters.command('deleteall') & filters.user(ADMINS))
async def delete_all_index(bot, message):
    await message.reply_text(
        'This will delete all indexed files.\nDo you want to continue??',
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text="YES", callback_data="autofilter_delete"
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="CANCEL", callback_data="close_data"
                    )
                ],
            ]
        ),
        quote=True,
    )


@Client.on_callback_query(filters.regex(r'^autofilter_delete'))
async def delete_all_index_confirm(bot, message):
    await Media.collection.drop()    
    await message.message.edit('Succesfully Deleted All The Indexed Files.')


@Client.on_message(filters.command('settings') & filters.private)
async def settings(client, message):
    userid = message.from_user.id if message.from_user else None
    if not userid:
        return await message.reply(f"You are anonymous admin. Use /connect {message.chat.id} in PM")
    chat_type = message.chat.type

    if chat_type == "private":
        grpid = await active_connection(str(userid))
        if grpid is not None:
            grp_id = grpid
            try:
                chat = await client.get_chat(grpid)
                title = chat.title
            except:
                await message.reply_text("Make sure I'm present in your group!!", quote=True)
                return
        else:
            await message.reply_text("I'm not connected to any groups!", quote=True)
            return

    elif chat_type in ["group", "supergroup"]:
        grp_id = message.chat.id
        title = message.chat.title

    else:
        return

    st = await client.get_chat_member(grp_id, userid)
    if (
            st.status != "administrator"
            and st.status != "creator"
            and str(userid) not in ADMINS
    ):
        return
    settings = await get_settings(grp_id)
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
                InlineKeyboardButton('Cʜᴀᴛ' if settings["botpm"] else 'Pᴍ',
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
        if settings["button"]:
            stats="Sɪɴɢʟᴇ"
        else:
            stats="Dᴏᴜʙʟᴇ"
        if settings["botpm"]:
            stats2="Cʜᴀᴛ"
        else:
            stats2="Pᴍ"
        if settings["file_secure"]:
            stats3="Yᴇs"
        else:
            stats3="Nᴏ"
        if settings["imdb"]:
            stats4="Yᴇs"
        else:
            stats4="Nᴏ"
        if settings["spell_check"]:
            stats5="Nᴇᴡ"
        else:
            stats5="Dᴇғᴀᴜʟᴛ"
        if settings["welcome"]:
            stats6="Yᴇs"
        else:
            stats6="Nᴏ"
        await message.reply_text(
            text=f"<b><u>Cᴜʀʀᴇɴᴛ sᴇᴛᴛɪɴɢs Fᴏʀ {title}</u></b>\n\nFɪʟᴛᴇʀ Bᴜᴛᴛᴏɴ : {stats}\nRᴇᴅɪᴇʀᴄᴛ Tᴏ : {stats2}\nFɪʟᴇ Sᴇᴄᴄʀᴇ : {stats3}\nIᴍᴅʙ : {stats4}\nSᴘᴇʟʟ Cʜᴇᴄᴋ : {stats5}\nWᴇʟᴄᴏᴍ : {stats6}\n\n<b>Hᴇʏ Bᴜᴅᴅʏ Hᴇʀᴇ Yᴏᴜ Cᴀɴ Cʜᴀɴɢᴇ Sᴇᴛᴛɪɴɢs As Yᴏᴜʀ Wɪsʜ Bʏ Usɪɴɢ Bᴇʟᴡ Bᴜᴛᴛᴏɴs</b>",
            reply_markup=reply_markup,
            disable_web_page_preview=True,
            parse_mode="html",
            reply_to_message_id=message.message_id
        )
@Client.on_message(filters.command('settings') & filters.group)
async def settings2(client, message):
    userid = message.from_user.id if message.from_user else None
    if not userid:
        return await message.reply(f"You are anonymous admin. Use /connect {message.chat.id} in PM")
    chat_type = message.chat.type

    if chat_type == "private":
        grpid = await active_connection(str(userid))
        if grpid is not None:
            grp_id = grpid
            try:
                chat = await client.get_chat(grpid)
                title = chat.title
            except:
                await message.reply_text("Make sure I'm present in your group!!", quote=True)
                return
        else:
            await message.reply_text("I'm not connected to any groups!", quote=True)
            return

    elif chat_type in ["group", "supergroup"]:
        grp_id = message.chat.id
        title = message.chat.title

    else:
        return

    st = await client.get_chat_member(grp_id, userid)
    if (
            st.status != "administrator"
            and st.status != "creator"
            and str(userid) not in ADMINS
    ):
        return
    settings = await get_settings(grp_id)
    if settings is not None:
        buttons = [[
            InlineKeyboardButton('🗣️ Oᴘᴇɴ Iɴ Pʀɪᴠᴀᴛᴇ Cʜᴀᴛ', callback_data="set2")
        ],
        [
            InlineKeyboardButton('👥 Oᴘᴇɴ Hᴇʀᴇ', callback_data='setgs')
        ]]
        reply_markup=InlineKeyboardMarkup(buttons)
        nl = await message.reply_text(
            text="<b>Hᴇʏ Bᴜᴅᴅʏ Wʜᴇʀᴇ Dᴏ Yᴏᴜ Wᴀɴᴛ Tᴏ Oᴘᴇɴ Sᴇᴛᴛɪɴɢs ⚙️</b>",
            reply_markup=reply_markup,
            parse_mode='html'
        )
        await asyncio.sleep(300)
        await message.delete()
        await nl.delete()
        del message, nl


