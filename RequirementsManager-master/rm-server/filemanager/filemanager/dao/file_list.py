from typing import List

from pymongo.collection import Collection

from filemanager.dao.file import File

class FileListDao:
    def get_all_files(self):
        pass

    def get_all_files_by_ids(self,file_ids:List[str]):
        pass

class FileListMongoDBDao(FileListDao):
    def __init__(self,collection:Collection):
        self.collection=collection

    def get_all_files(self):
        files=self.collection.find()
        res=[]
        for file in files:
            res.append(File(**file))
        return res

    def get_all_files_by_ids(self,file_ids:List[str]):
        files=self.collection.find({'_id':{'$in':file_ids}})
        return [File(**file) for file in files]