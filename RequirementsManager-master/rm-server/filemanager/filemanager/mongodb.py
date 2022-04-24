import pymongo

from filemanager.config import  MONGODB_URL

client=pymongo.MongoClient(MONGODB_URL)
database=client['FileManager']
file_collection=database['File']


