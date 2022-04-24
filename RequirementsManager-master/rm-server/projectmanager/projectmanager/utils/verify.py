from projectmanager.mongodb import (
    project_collection, project_userlist_collection
)
from projectmanager.dao.project import ProjectMongoDBDao
from projectmanager.dao.project_userlist import (
    ProjectUserListMongoDBDao
)


def verify_project_exist(project_id: str) -> bool:
    project_dao = ProjectMongoDBDao(project_collection)
    project = project_dao.get_project(project_id)
    if not project:
        return False
    return True


def verify_project_user_role_access(project_id: str,
                                    username: str,
                                    access: str) -> bool:
    project_userlist_dao = ProjectUserListMongoDBDao(
        project_userlist_collection
    )
    return project_userlist_dao.check_access(
        project_id, username, access
    )
