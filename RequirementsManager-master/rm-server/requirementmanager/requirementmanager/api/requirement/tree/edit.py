from datetime import datetime

from flask import request

from requirementmanager.app import app
from requirementmanager.mongodb import (
    requirement_collection, requirement_tree_collection
)
from requirementmanager.dao.requirement_list import (
    RequirementListMongoDBDao
)
from requirementmanager.dao.requirement_tree import (
    RequirementTreeMongoDBDao
)
from requirementmanager.utils.handle_api import handle_response, verify_request


META_SUCCESS = {'status': 200, 'msg': '修改成功！'}


@app.route('/requirement/tree/edit', methods=['PUT'])
@verify_request(['access'], access='requirement_tree_edit')
@handle_response
def requirement_tree_edit():
    body = request.json

    # 获取body
    project_id = body['project_id']
    requirement_id = body['requirement_id']
    base_id = body['base_id']
    location = body['location']

    requirement_list_dao = RequirementListMongoDBDao(
        requirement_collection
    )
    requirement_tree_dao = RequirementTreeMongoDBDao(
        requirement_tree_collection
    )

    # 修改需求树
    requirement_tree_dao.edit_tree_node(
        project_id, requirement_id, base_id, location
    )

    # 修改需求类型和最后修改日期
    tree = requirement_tree_dao.get(project_id)
    requirement_ids = tree.get_children_ids(requirement_id) + [requirement_id]
    new_type = tree.get_node_type(requirement_id)
    last_modify_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    requirement_list_dao.batch_edit_requirements(
        requirement_ids, _type=new_type, last_modify_time=last_modify_time
    )

    return {
        'meta': META_SUCCESS
    }
