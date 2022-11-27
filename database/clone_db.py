import pymongo
from info import DATABASE_URI2

#-------------»[Create_DB]«--------------#

myclient = pymongo.MongoClient(DATABASE_URI2)
db_x = myclient["Nl_Clone_Bot"]
clonedb = db_x["clone_db"]
string = db_x["STRING"]

#-------------»[Saving_DB]«-------------#

async def add_bot(user_id, client):
    await string.insert_one({"_id": user_id, "string": client})

async def get_bot(user_id):
    text = string.find_one({"_id": user_id})
    return text

async def rmsession(client):
    await string.delete_one({"string": client})


async def get_all_bot():
    lol = [n for n in string.find({})]
    return lol

async def is_session_in_db(client):
    k = await string.find_one({"string": client})
    if k:
        return True
    else:
        return False

async def count_bot():
    b_count=await string.count_documents({})
    return b_count


async def add_stext(id, text):	
    await clonedb.update_one({'id' : id}, {'$set' : {'text' : text}})

async def get_stext(id):
    bot = clonedb.find_one({'id' : int(id)})
    return bot
