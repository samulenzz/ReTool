from projectmanager.mongodb import (
    project_collection, project_userlist_collection, baseline_collection
)

if __name__ == '__main__':
    project_collection.drop()
    project_userlist_collection.drop()
    baseline_collection.drop()
