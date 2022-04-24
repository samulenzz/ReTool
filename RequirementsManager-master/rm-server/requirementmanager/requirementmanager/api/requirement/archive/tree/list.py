from flask import request

from requirementmanager.app import app
from requirementmanager.dao.archive import (
    ArchiveRequirementTreeMongoDBDao
)
from requirementmanager.mongodb import archive_requirement_tree_collection
from requirementmanager.utils.handle_api import handle_response, verify_request
from requirementmanager.utils.wrap_elementui_tree import add_section_number


META_SUCCESS = {'status': 200, 'msg': '获取成功！'}


@app.route('/requirement/archive/tree/list', methods=['GET'])
@verify_request(['access'], access='requirement_archive_tree_list')
@handle_response
def requirement_archive_tree_list():
    project_id = request.args.get('project_id')
    version = request.args.get('version')

    archive_requirement_tree_dao = ArchiveRequirementTreeMongoDBDao(
        archive_requirement_tree_collection
    )

    tree = archive_requirement_tree_dao.get(project_id, version)

    resp_data = tree.get_elementui_tree()
    add_section_number(resp_data, 1)

    return {
        'meta': META_SUCCESS,
        'data': resp_data
    }
