from projectmanager.mongodb import (
    project_collection, project_userlist_collection, baseline_collection
)
from projectmanager.dao.project import (
    Project, ProjectMongoDBDao
)
from projectmanager.dao.project_userlist import (
    ProjectUser, ProjectUserListMongoDBDao,
    PROJECT_ROLE_PROJECT_MANAGER
)
from projectmanager.dao.project_list import ProjectListMongoDBDao
from projectmanager.dao.baseline import BaselineMongoDBDao


if __name__ == '__main__':
    # 创建项目
    project = Project(
        project_name='示例项目',
        description='这是示例项目',
        status='进行中'
    )
    project_dao = ProjectMongoDBDao(project_collection)
    project_dao.create_project(project)

    # 添加用户
    project_user = ProjectUser(
        username='admin',
        project_role=PROJECT_ROLE_PROJECT_MANAGER
    )
    project_userlist_dao = ProjectUserListMongoDBDao(
        project_userlist_collection
    )
    project_userlist_dao.create(project._id)
    project_userlist_dao.edit_users(project._id, [project_user])
    print(project_userlist_dao.get_all_users(project._id))

    project_list_dao = ProjectListMongoDBDao(project_collection)
    print(project_list_dao.get_all_projects())

    # 初始化基线
    baseline_dao = BaselineMongoDBDao(baseline_collection)
    baseline_dao.create(project._id)
    print(baseline_dao.get_all_nodes(project._id))
