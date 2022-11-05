from pyrogram import *
from pyrogram.types import *


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
       
       
       
       
       
       
       
       
       
       
     
     
     
     
     
     
     
