from filemanager.mongodb import (file_collection)
from filemanager.dao.file import FileMongoDBDao


def verify_file_exist(file_id:str):
    file_dao=FileMongoDBDao(file_collection)
    file=file_dao.get_file(file_id)
    if not file:
        return False
    return True
