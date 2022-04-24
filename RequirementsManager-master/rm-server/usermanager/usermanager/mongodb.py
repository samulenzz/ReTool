import pymongo

from usermanager.config import MONGODB_URL


client = pymongo.MongoClient(MONGODB_URL)
database = client['RequirementsManager']
user_collection = database['User']
