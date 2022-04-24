from typing import List
from datetime import datetime

from flask import request

from requirementmanager.app import app
from requirementmanager.utils.handle_api import handle_response, verify_request
from requirementmanager.mongodb import (
    requirement_collection, requirement_tree_collection
)
from requirementmanager.dao.requirement_list import (
    Requirement, RequirementListMongoDBDao
)
from requirementmanager.dao.requirement_tree import (
    RequirementTree, RequirementTreeNode, RequirementTreeMongoDBDao
)
from requirementmanager.utils.client_username import get_client_username


META_SUCCESS = {'status': 200, 'msg': '创建成功！'}


def wrap_name(name: str) -> str:
    name = name.split(' ', 1)[-1]
    if len(name) <= 10:
        return name
    return f'{name[:7]}...'


def wrap_description(description: str) -> str:
    return description.split(' ', 1)[-1]


def gen_requirements_list(res: List, node_list: List, project_id: str,
                          _type: str, author: str, timestamp: str):
    for node in node_list:
        requirement = Requirement(
            project_id=project_id,
            name=wrap_name(node['label']),
            description=wrap_description(node['label']),
            _id=node['_id'],
            _type=_type,
            author=author,
            created_time=timestamp,
            last_modify_time=timestamp,
        )
        res.append(requirement)
        gen_requirements_list(
            res, node['children'], project_id,
            _type, author, timestamp
        )


def add_to_tree(tree: RequirementTree,
                node_list: List, base_id: str):
    print(node_list)
    for node in node_list:
        tree_node = RequirementTreeNode(
            _id=node['_id'],
            name=wrap_name(node['label']),
        )
        tree.add_node(tree_node, base_id, 'inner')
        add_to_tree(tree, node['children'], node['_id'])


@app.route('/requirement/importfile/create', methods=['POST'])
@verify_request(['access'], access='requirement_importfile_create')
@handle_response
def requirement_importfile_create():
    body = request.json
    project_id = body['project_id']
    elementui_tree = body['tree']
    client_username = get_client_username()
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    requirement_list_dao = RequirementListMongoDBDao(
        requirement_collection
    )
    requirement_tree_dao = RequirementTreeMongoDBDao(
        requirement_tree_collection
    )

    # 获取需求条目, 批量添加至数据库
    # tree的根节点一定是需求类型，遍历需求类型添加
    requirements = []
    for node in elementui_tree:
        gen_requirements_list(
            requirements, node['children'], project_id,
            node['_id'], client_username, timestamp
        )
    print(requirements)
    requirement_list_dao.batch_create_requirements(requirements)

    # 依次添加至需求树中
    tree = requirement_tree_dao.get(project_id)
    # 如果不存在就创建
    if not tree:
        tree = RequirementTree(project_id)
        requirement_tree_dao.create(tree)
    for node in elementui_tree:
        add_to_tree(tree, node['children'], node['_id'])
    requirement_tree_dao.edit(
        project_id, requirement_nodes=tree.requirement_nodes
    )

    return {
        'meta': META_SUCCESS
    }
