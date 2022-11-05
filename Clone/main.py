from pyrogram import *
from pyrogram.types import *

@Client.on_message(filters.command(['start']) & filters.private)
async def clone_start(bot, msg):
 
  btn = [[
      InlineKeyboardButton('❗Hᴇʟᴘ', callback_data="help"),
      InlineKeyboardButton('😎 Aʙᴏᴜᴛ', callback_data="about")
  ]]
  await msg.reply_text(
      text = f"<b>Yᴏ Yᴏ !\nIᴀᴍ A Sɪᴍᴘʟᴇ Aᴜᴛᴏ Fɪʟᴛᴇ + Fɪʟᴇ Sʜᴀʀᴇ Bᴏᴛ...</b>",
      reply_markup = InlineKeyboardMarkup(btn)
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
        imdb2 = await get_poster(search)
        cap2 = script.IMDB_MOVIE_2.format(query=search, title=imdb2['title'], rating=imdb2['rating'], genres=imdb2['genres'], year=imdb2['release_date'], runtime=imdb2['runtime'], language=imdb2['languages'], group=message.chat.title, url="https://t.me/cinema_lookam", short=imdb2['plot']) if imdb2 else f"𝗙𝗶𝗹𝗺 : <b>{search}</b>\n𝗬𝗲𝗮𝗿 : <code>N/A</code>\n𝗥𝗮𝘁𝗶𝗻𝗴 : <code>N/A</code>\n𝗟𝗮𝗻𝗴𝘂𝗮𝗴𝗲 : <code>N/A</code>\n\n©️ 𝗧𝗲𝗮𝗺 <a href=https://t.me/cinema_lookam><b>{message.chat.title}</b></a> ™️"
    
    if imdb and imdb.get('poster'):                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 
        try:
            fmsg = await message.reply_photo(photo=imdb.get('poster'), caption=cap1[:1024],
                                      reply_markup=InlineKeyboardMarkup(btn))
        except (MediaEmpty, PhotoInvalidDimensions, WebpageMediaEmpty):
            pic = imdb.get('poster')
            poster = pic.replace('.jpg', "._V1_UX360.jpg")
            fmsg = await message.reply_photo(photo=poster, caption=cap1[:1024], reply_markup=InlineKeyboardMarkup(btn))
        except Exception as e:
            logger.exception(e)
            fmsg = await message.reply_photo(photo=random.choice(REQ_PIC), caption=cap2, reply_markup=InlineKeyboardMarkup(btn))
    else:
        imdb2 = await get_poster(search)
        fmsg = await message.reply_photo(photo=random.choice(REQ_PIC), caption=cap2, reply_markup=InlineKeyboardMarkup(btn))
    await asyncio.sleep(DELETE_TIME)
    await message.delete()
    await fmsg.delete()
  
    if spoll:
        await msg.message.delete()
