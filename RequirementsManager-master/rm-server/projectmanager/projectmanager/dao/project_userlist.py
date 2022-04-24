from dataclasses import dataclass, field
from typing import List

from pymongo.collection import Collection


# 用户项目内角色
PROJECT_ROLE_PROJECT_MANAGER = '项目经理'
PROJECT_ROLE_PROJECT_LEADER = '项目组长'
PROJECT_ROLE_COMMON_USER = '普通成员'


# 角色对应的权限
PROJECT_ROLE_ACCESS = {
    PROJECT_ROLE_PROJECT_MANAGER: [
        'project_delete',
        'project_edit',
        'project_profile',
        'project_user_edit',
        'project_user_list',
        'project_baseline_node_create',
        'project_baseline_node_list',
        'requirement_create',
        'requirement_delete',
        'requirement_edit',
        'requirement_profile',
        'requirement_tree_edit',
        'requirement_tree_list',
        'requirement_importfile_create',
        'requirement_archive_profile',
        'requirement_archive_tree_list',
    ],
    PROJECT_ROLE_PROJECT_LEADER: [
        'project_profile',
        'project_user_list',
        'project_baseline_node_list',
        'requirement_create',
        'requirement_delete',
        'requirement_edit',
        'requirement_profile',
        'requirement_tree_edit',
        'requirement_tree_list',
        'requirement_importfile_create',
        'requirement_archive_profile',
        'requirement_archive_tree_list',
    ],
    PROJECT_ROLE_COMMON_USER: [
        'project_profile',
        'project_user_list',
        'project_baseline_node_list',
        'requirement_profile',
        'requirement_tree_list',
        'requirement_archive_profile',
        'requirement_archive_tree_list',
    ],
}


@dataclass
class ProjectUser:
    username: str
    project_role: str

    def jsonify(self):
        return {
            'username': self.username,
            'project_role': self.project_role
        }


@dataclass
class ProjectUserList:
    project_id: str
    users: List[ProjectUser] = field(default_factory=list)

    def jsonify(self):
        return {
            '_id': self.project_id,
            'users': [user.jsonify() for user in self.users]
        }


class ProjectUserListDao:
    def create(self, project_id: str):
        pass

    def delete(self, project_id: str):
        pass

    def edit_users(self, project_id: str, users: List[ProjectUser]):
        pass

    def get_user(self, project_id: str, username: str) -> ProjectUser:
        pass

    def get_all_users(self, project_id: str) -> List[ProjectUser]:
        pass

    def get_projects_by_user(self, username: str) -> List[str]:
        pass

    def check_access(self, project_id: str, username: str, access: str) -> bool:
        pass


class ProjectUserListMongoDBDao(ProjectUserListDao):
    def __init__(self, collection: Collection):
        self.collection = collection

    def create(self, project_id: str):
        project_userlist = ProjectUserList(project_id)
        self.collection.insert_one(project_userlist.jsonify())

    def delete(self, project_id: str):
        self.collection.delete_one({'_id': project_id})

    def edit_users(self, project_id, users: List[ProjectUser]):
        users = [user.jsonify() for user in users]
        new_users = {"$set": {'users': users}}
        self.collection.update({'_id': project_id}, new_users)

    def get_user(self, project_id: str, username: str) -> ProjectUser:
        projectuser_dict = self.collection.find_one({'_id': project_id})
        for user in projectuser_dict['users']:
            if user['username'] == username:
                return ProjectUser(**user)
        return None

    def get_all_users(self, project_id: str) -> List[ProjectUser]:
        projectuser_dict = self.collection.find_one({'_id': project_id})
        res = []
        for user in projectuser_dict['users']:
            res.append(ProjectUser(**user))
        return res

    def get_projects_by_user(self, username: str) -> List[str]:
        condition = {'users': {'$elemMatch': {'username': username}}}
        projects = self.collection.find(condition)
        return [project['_id'] for project in projects]

    def check_access(self, project_id: str, username: str, access: str) -> bool:
        user = self.get_user(project_id, username)
        if not user:
            return False
        role = user.project_role
        is_access = access in PROJECT_ROLE_ACCESS[role]
        return is_access
