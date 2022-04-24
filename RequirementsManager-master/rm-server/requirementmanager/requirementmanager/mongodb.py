import pymongo

from requirementmanager.config import MONGODB_URL


client = pymongo.MongoClient(MONGODB_URL)
database = client['RequirementsManager']
requirement_collection = database['Requirement']
archive_requirement_collection = database['ArchiveRequirement']
requirement_tree_collection = database['RequirementTree']  # 存储需求树的结构
archive_requirement_tree_collection = database['ArchiveRequirementTree']
