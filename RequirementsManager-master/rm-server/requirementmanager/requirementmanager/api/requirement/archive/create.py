from flask import request

from requirementmanager.app import app
from requirementmanager.mongodb import (
    requirement_collection, archive_requirement_collection,
    requirement_tree_collection, archive_requirement_tree_collection
)
from requirementmanager.dao.requirement_list import RequirementListMongoDBDao
from requirementmanager.dao.requirement_tree import (
    RequirementTreeMongoDBDao
)
from requirementmanager.dao.archive import (
    ArchiveRequirement, ArchiveRequirementListMongoDBDao,
    ArchiveRequirementTree, ArchiveRequirementTreeMongoDBDao
)
from requirementmanager.utils.handle_api import handle_response


META_SUCCESS = {'status': 200, 'msg': '创建成功！'}
META_ERROR = {'status': 400, 'msg': '创建失败！当前项目没有需求'}


@app.route('/requirement/archive/create', methods=['POST'])
@handle_response
def requirement_archive_create():
    body = request.json
    version = body['version']
    project_id = body['project_id']

    requirement_list_dao = RequirementListMongoDBDao(
        requirement_collection
    )
    archive_requirement_list_dao = ArchiveRequirementListMongoDBDao(
        archive_requirement_collection
    )
    requirement_tree_dao = RequirementTreeMongoDBDao(
        requirement_tree_collection
    )
    archive_requirement_tree_dao = ArchiveRequirementTreeMongoDBDao(
        archive_requirement_tree_collection
    )

    # 根据project id获取所有需求
    reqs = requirement_list_dao.get_requirement_list(project_id=project_id)
    if len(reqs) == 0:
        return {
            'meta': META_ERROR
        }

    archive_reqs = [
        ArchiveRequirement.import_requirement(req, version) for req in reqs
    ]
    # 转换后批量添加至数据库
    archive_requirement_list_dao.batch_create_requirements(archive_reqs)

    # 归档Tree
    tree = requirement_tree_dao.get(project_id)
    archive_tree = ArchiveRequirementTree.import_requirement_tree(tree, version)
    archive_requirement_tree_dao.create(archive_tree)

    return {
        'meta': META_SUCCESS
    }
