import pymongo
from info import DATABASE_URI2

#-------------»[Create_DB]«--------------#

myclient = pymongo.MongoClient(DATABASE_URI2)
db_x = myclient["Nl_Clone_Bot"]

###_________»[Storage]«______________###

string = db_x["STRING"]

async def add_bot(user_id, client):
    await string.insert_one({"_id": user_id, "string": client})

async def rmsession(client):
    await string.delete_one({"string": client})

async def del_session_id(user_id):
    await string.delete_one({"_id": user_id})

async def rm_all_session():
    await string.delete_many({})

async def get_all_bot():
    lol = [n for n in string.find({})]
    return lol

async def get_bot(user_id):
    bt = await string.find_one({"string": user_id})
    return bt

async def is_session_in_db(client):
    k = await string.find_one({"string": client})
    if k:
        return True
    else:
        return False

async def userid_in_db(user_id):
    man = await string.find_one({"_id": user_id})
    if man:
        return True
    else:
        return False
