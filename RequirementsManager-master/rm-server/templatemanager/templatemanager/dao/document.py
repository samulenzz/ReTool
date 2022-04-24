from dataclasses import dataclass
from typing import Dict, List, Tuple

from pymongo.collection import Collection

from templatemanager.utils.uuid import generate_uuid

from time import asctime, localtime


@dataclass
class Document:
    _id: str
    document_name: str
    template_name: str
    introduction: str
    last_time: str
    outline: List
    contents: List
    comments_file_list: List[str]

    # def __init__(self, document_name: str = "", template_name: str = "", introduction: str = "", outline: list = []):
    #     # typing declaration
    #     self.id: str
    #     self.document_name: str
    #     self.template_name: str
    #     self.introduction: str
    #     self.last_time: str
    #     self.contents: List[Tuple]
    #     self.comments_file_list: List[str]
    #     # assignment
    #     self.id = generate_uuid()
    #     self.document_name = document_name
    #     self.template_name = template_name
    #     self.introduction = introduction
    #     self.last_time = asctime(localtime())
    #     self.contents = []
    #     for line in outline:
    #         self.contents.append((line, ""))
    #     self.comments_file_list = []

    def jsonify(self) -> Dict:
        return {
            "_id": self._id,
            "document_name": self.document_name,
            "template_name": self.template_name,
            "introduction": self.introduction,
            "last_time": self.last_time,
            "outline": self.outline,
            "contents": self.contents,
            "comments_file_list": self.comments_file_list
        }


class DocumentDao:
    def create_document(self, document: Document):
        pass

    def delete_document(self, _id: str):
        pass

    def edit_document(self, _id: str, attributes: Dict):
        pass

    def get_document(self, _id: str) -> Document:
        pass

    def get_all_document(self) -> List[Document]:
        pass


class DocumentMongoDBDao(DocumentDao):
    def __init__(self, collection: Collection):
        self.collection = collection

    def create_document(self, document: Document):
        self.collection.insert_one(document.jsonify())

    def delete_document(self, document_id: str):
        self.collection.delete_one({'_id': document_id})

    def edit_document(self, document_id: str, attributes: Dict):
        new_values = {'$set': attributes}
        self.collection.update_one(
            {'_id': document_id},
            new_values
        )

    def get_document(self, document_id: str) -> Document:
        document_dict = self.collection.find_one(
            {'_id': document_id}
        )
        document = None
        if document_dict:
            document = Document(**document_dict)
            # document.__dict__.update(document_dict)
        return document

    def get_all_document(self) -> List[Document]:
        document_list = self.collection.find()
        res = []
        for document_dict in document_list:
            doc = Document(**document_dict)
            # doc.__dict__.update(document_dict)
            res.append(doc)
        return res
