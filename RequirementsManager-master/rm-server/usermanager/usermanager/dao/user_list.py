from typing import List

from pymongo.collection import Collection

from usermanager.dao.user import User


class UserListDao:
    def get_all_users(self) -> List[User]:
        pass


class UserListMongoDBDao(UserListDao):
    def __init__(self, collection: Collection):
        self.collection = collection

    def get_all_users(self) -> List[User]:
        users_list = self.collection.find()
        res = []
        for user_dict in users_list:
            user_dict.pop('_id')
            res.append(User(**user_dict))
        return res
