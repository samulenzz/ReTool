import pymongo

from projectmanager.config import MONGODB_URL


client = pymongo.MongoClient(MONGODB_URL)
database = client['RequirementsManager']
project_collection = database['Project']
project_userlist_collection = database['ProjectUserList']
baseline_collection = database['Baseline']
