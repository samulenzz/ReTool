from dataclasses import dataclass

from pymongo.collection import Collection

from filemanager.utils.uuid import generate_uuid


@dataclass
class File:
    file_name:str
    _id:str=None
    description:str=None
    # fresid:str=None
    def __post_init__(self):
        if not self._id:
            self._id = generate_uuid()
    def jsonify(self):
        return {
            '_id':self._id,
            'file_name':self.file_name,
            'description':self.description,
            # 'fresid':self.fresid
        }

class FileDao:
    def create_file(self,file:File):
        pass

    def delete_file(self,_id:str):
        pass

    def edit_file(self,_id:str,**attributes):
        pass

    def get_file(self,_id:str)->File:
        pass

class FileMongoDBDao(FileDao):
    def __init__(self,collection:Collection):
        self.collection=collection

    def create_file(self,file:File):
        self.collection.insert_one(file.jsonify())

    def delete_file(self,_id:str):
        self.collection.delete_one({'_id':_id})

    def get_file(self,_id:str) ->File:
        file_dict=self.collection.find_one({'_id':_id})

        if file_dict:
            file=File(**file_dict)
        else:
            file=None

        return file