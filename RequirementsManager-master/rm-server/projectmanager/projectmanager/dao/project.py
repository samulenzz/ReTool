from dataclasses import dataclass

from pymongo.collection import Collection

from projectmanager.utils.uuid import generate_uuid


@dataclass
class Project:
    project_name: str
    _id: str = None
    description: str = None
    start_time: str = None
    status: str = None

    def __post_init__(self):
        if not self._id:
            self._id = generate_uuid()

    def jsonify(self):
        return {
            '_id': self._id,
            'project_name': self.project_name,
            'description': self.description,
            'start_time': self.start_time,
            'status': self.status,
        }


class ProjectDao:
    def create_project(self, project: Project):
        pass

    def delete_project(self, _id: str):
        pass

    def edit_project(self, _id: str, **attributes):
        pass

    def get_project(self, _id: str) -> Project:
        pass


class ProjectMongoDBDao(ProjectDao):
    def __init__(self, collection: Collection):
        self.collection = collection

    def create_project(self, project: Project):
        self.collection.insert_one(project.jsonify())

    def delete_project(self, _id: str):
        self.collection.delete_one({'_id': _id})

    def edit_project(self, _id: str, **attributes):
        new_values = {'$set': attributes}
        self.collection.update_one({'_id': _id}, new_values)

    def get_project(self, _id: str) -> Project:
        project_dict = self.collection.find_one({'_id': _id})
        if project_dict:
            project = Project(**project_dict)
        else:
            project = None
        return project
