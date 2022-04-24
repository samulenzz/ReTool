from typing import List

from pymongo.collection import Collection

from requirementmanager.dao.requirement import Requirement


class RequirementListDao:
    def get_requirement_list(self, **attributes) -> List[Requirement]:
        pass

    def batch_create_requirements(self, requirements: List[Requirement]):
        pass


class RequirementListMongoDBDao(RequirementListDao):
    def __init__(self, collection: Collection):
        self.collection = collection

    def get_requirement_list(self, **attributes) -> List[Requirement]:
        condition = {}
        if 'project_id' in attributes:
            condition['project_id'] = attributes['project_id']
        requirements = self.collection.find(condition)

        res = []
        for requirement in requirements:
            res.append(Requirement(**requirement))

        return res

    def batch_create_requirements(self, requirements: List[Requirement]):
        requirements_dict = [
            requirement.jsonify()
            for requirement in requirements
        ]
        self.collection.insert_many(requirements_dict)

    def batch_edit_requirements(self, ids: List[str], **attributes):
        new_values = {'$set': attributes}
        self.collection.update_many({'_id': {'$in': ids}}, new_values)
