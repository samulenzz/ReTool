from typing import List

from pymongo.collection import Collection

from projectmanager.dao.project import Project


class ProjectListDao:
    def get_all_projects(self) -> List[Project]:
        pass

    def get_projects_by_ids(self, project_ids: List[str]) -> List[Project]:
        pass


class ProjectListMongoDBDao(ProjectListDao):
    def __init__(self, collection: Collection):
        self.collection = collection

    def get_all_projects(self) -> List[Project]:
        projects = self.collection.find()
        res = []
        for project in projects:
            res.append(Project(**project))
        return res

    def get_projects_by_ids(self, project_ids: List[str]) -> List[Project]:
        projects = self.collection.find({'_id': {'$in': project_ids}})
        return [Project(**project_dict) for project_dict in projects]
