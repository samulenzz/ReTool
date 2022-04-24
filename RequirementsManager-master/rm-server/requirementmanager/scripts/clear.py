from requirementmanager.mongodb import (
    requirement_collection, requirement_tree_collection,
    archive_requirement_collection, archive_requirement_tree_collection
)

if __name__ == '__main__':
    requirement_collection.drop()
    requirement_tree_collection.drop()
    archive_requirement_collection.drop()
    archive_requirement_tree_collection.drop()
