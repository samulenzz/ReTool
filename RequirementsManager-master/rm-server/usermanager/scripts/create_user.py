from usermanager.mongodb import user_collection
from usermanager.dao.user import (
    User, UserMongoDBDao, SYSTEM_ROLE_SYSTEM_MANAGER, SYSTEM_ROLE_COMMON_USER
)
from usermanager.utils.password import encrypt_password


if __name__ == '__main__':
    user_collection.drop()
    user1 = User(
        username='admin',
        password=encrypt_password('123456'),
        system_role=SYSTEM_ROLE_SYSTEM_MANAGER,
        email='example@qq.com',
        phone_number='123456789'
    )
    user2 = User(
        username='changliu',
        password=encrypt_password('123456'),
        system_role=SYSTEM_ROLE_SYSTEM_MANAGER,
        email='example@qq.com',
        phone_number='123456789'
    )
    user3 = User(
        username='张三',
        password=encrypt_password('123456'),
        system_role=SYSTEM_ROLE_SYSTEM_MANAGER,
        email='example@qq.com',
        phone_number='123456789'
    )
    user4 = User(
        username='李四',
        password=encrypt_password('123456'),
        system_role=SYSTEM_ROLE_COMMON_USER,
        email='example@qq.com',
        phone_number='123456789'
    )

    user_mongo_dao = UserMongoDBDao(user_collection)
    user_mongo_dao.create_user(user1)
    user_mongo_dao.create_user(user2)
    user_mongo_dao.create_user(user3)
    user_mongo_dao.create_user(user4)
