from typing import List, Dict

from requirementmanager.mongodb import (
    requirement_tree_collection
)
from requirementmanager.dao.requirement_tree import (
    RequirementTreeMongoDBDao
)
from requirementmanager.utils.uuid import generate_uuid


def wrap_add_single_requirement(target_data: Dict):
    """
    target_data:
    {
        "project_id": str,
        "base_id": str,
        "name": str,
        "description: str
    }
    """
    project_id = target_data['project_id']
    base_id = target_data['base_id']
    requirement_id = generate_uuid()
    requirement_tree_dao = RequirementTreeMongoDBDao(
        requirement_tree_collection
    )
    _type = requirement_tree_dao.get(project_id).get_node_type(base_id)
    return {
        requirement_id: {
            'id': requirement_id,
            'name': target_data['name'],
            'description': target_data['description'],
            'type': _type
        }
    }


def wrap_name(name: str) -> str:
    name = name.split(' ', 1)[-1]
    if len(name) <= 10:
        return name
    return f'{name[:7]}...'


def wrap_description(description: str) -> str:
    return description.split(' ', 1)[-1]


def _add_requirement(res, node_list, _type: str):
    for node in node_list:
        res[node['_id']] = {
            'id': node['_id'],
            'name': wrap_name(node['label']),
            'description': wrap_description(node['label']),
            'type': _type
        }
        _add_requirement(res, node['children'], _type)


def wrap_tree_requirements(target_data: List):
    res = {}
    for item in target_data:
        _add_requirement(res, item['children'], item['_id'])
    return res


def wrap_edit_single_requirement(target_data: Dict):
    return {
        target_data['_id']: {
            'id': target_data['_id'],
            'name': target_data['name'],
            'description': target_data['description'],
            'type': target_data['_type']
        }
    }


def wrap_compared_requirements(requirements: List):
    res = {}
    for req in requirements:
        res[req._id] = {
            'id': req._id,
            'name': req.name,
            'description': req.description,
            'type': req._type
        }
    return res
