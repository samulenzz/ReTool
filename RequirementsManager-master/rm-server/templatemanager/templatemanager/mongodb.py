import pymongo

from templatemanager.config import MONGODB_URL


client = pymongo.MongoClient(MONGODB_URL)
database = client['RequirementsManager']
template_collection = database['Template']
document_collection = database['Document']
