import asyncio
import logging
import logging.config

# Get logging configurations
logging.config.fileConfig('logging.conf')
logging.getLogger().setLevel(logging.INFO)
logging.getLogger("pyrogram").setLevel(logging.ERROR)
logging.getLogger("imdbpy").setLevel(logging.ERROR)

from pyrogram import Client, __version__
from pyrogram.raw.all import layer
from database.ia_filterdb import Media
from database.users_chats_db import db
from info import SESSION, API_ID, API_HASH, BOT_TOKEN, LOG_STR
from utils import temp
from database.clone_db import get_all_bot
import pyromod.listen


class Bot(Client):

    def __init__(self):
        super().__init__(
            name=SESSION,
            api_id=API_ID,
            api_hash=API_HASH,
            bot_token=BOT_TOKEN,
            workers=100,
            plugins={"root": "plugins"},
            sleep_threshold=10,
        )

    async def start_bot():
        print("[INFO]: LOADING ASSISTANT DETAILS")
        string = await get_all_bot()
        for i in string:
            try:
                pyroman = Client(session_name=f"{i['string']}", api_id=API_ID, api_hash=API_HASH, plugins=dict(root=f"Clone"))
                await pyroman.start()
                user = await pyroman.get_me()
                temp.CL = user.id
                temp.C_NAME = user.username
                print(f"[INFO]: Started {user.first_name}")
            except BaseException as eb:
                print(eb)
        print(f"Total Client = {len(string)} User")
        await idle()
        
    async def start(self):
  
        b_users, b_chats = await db.get_banned()
        temp.BANNED_USERS = b_users
        temp.BANNED_CHATS = b_chats
        await super().start()
        await Media.ensure_indexes()
        
        me = await self.get_me()
        temp.ME = me.id
        temp.U_NAME = me.username
        temp.B_NAME = me.first_name
        self.username = '@' + me.username
        logging.info(f"{me.first_name} with for Pyrogram v{__version__} (Layer {layer}) started on {me.username}.")
        logging.info(LOG_STR)
        

    
    async def stop(self, *args):
        await super().stop()
        logging.info("Bot stopped. Bye.")
        
    
    
loop = asyncio.get_event_loop()
loop.run_until_complete(start_bot())

app = Bot()
app.run()


