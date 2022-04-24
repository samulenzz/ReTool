from dataclasses import dataclass
from typing import List

from requirementmanager.dao.requirement import (
    Requirement, RequirementMongoDBDao
)
from requirementmanager.dao.requirement_list import (
    RequirementListMongoDBDao
)
from requirementmanager.dao.requirement_tree import (
    RequirementTree, RequirementTreeMongoDBDao
)
from requirementmanager.utils.uuid import generate_uuid


@dataclass
class ArchiveRequirement(Requirement):
    requirement_id: str = None
    version: str = None

    @classmethod
    def import_requirement(cls, requirement: Requirement, version: str):
        json_requirement = requirement.jsonify()
        json_requirement['version'] = version
        json_requirement['requirement_id'] = json_requirement['_id']
        json_requirement['_id'] = generate_uuid()
        return cls(**json_requirement)

    def jsonify(self):
        res = super().jsonify()
        res['requirement_id'] = self.requirement_id
        res['version'] = self.version
        return res


class ArchiveRequirementMongoDBDao(RequirementMongoDBDao):
    def get(self, requirement_id: str, version: str) -> ArchiveRequirement:
        requirement_dict = self.collection.find_one(
            {'requirement_id': requirement_id, 'version': version}
        )
        return ArchiveRequirement(**requirement_dict)


class ArchiveRequirementListMongoDBDao(RequirementListMongoDBDao):
    def get_requirement_list(self, **attributes) -> List[ArchiveRequirement]:
        condition = {}
        if 'project_id' in attributes:
            condition['project_id'] = attributes['project_id']
        if 'version' in attributes:
            condition['version'] = attributes['version']
        requirements = self.collection.find(condition)

        res = []
        for requirement in requirements:
            res.append(ArchiveRequirement(**requirement))

        return res

    def batch_create_requirements(self,
                                  requirements: List[ArchiveRequirement]):
        requirements_dict = [
            requirement.jsonify()
            for requirement in requirements
        ]
        self.collection.insert_many(requirements_dict)


@dataclass
class ArchiveRequirementTree(RequirementTree):
    version: str = None

    @classmethod
    def import_requirement_tree(cls, tree: RequirementTree, version: str):
        json_requirement = tree.jsonify()
        json_requirement['version'] = version
        json_requirement['_id'] = generate_uuid()
        return cls(**json_requirement)

    def jsonify(self):
        res = super().jsonify()
        res['version'] = self.version
        return res


class ArchiveRequirementTreeMongoDBDao(RequirementTreeMongoDBDao):
    def get(self, project_id: str, version: str) -> ArchiveRequirementTree:
        tree_dict = self.collection.find_one(
            {'project_id': project_id, 'version': version}
        )
        if tree_dict:
            tree = ArchiveRequirementTree(**tree_dict)
        else:
            tree = None
        return tree
