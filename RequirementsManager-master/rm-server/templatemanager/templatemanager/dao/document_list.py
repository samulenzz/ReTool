from typing import List

from pymongo.collection import Collection

from templatemanager.dao.document import Document


class DocumentListDao:
    def get_all_document(self) -> List[Document]:
        pass


class DocumentListMongoDBDao(DocumentListDao):
    def __init__(self, collection: Collection):
        self.collection = collection

    def get_all_document(self) -> List[Document]:
        document_list = self.collection.find()
        res = []
        for document_dict in document_list:
            res.append(Document(**document_dict))
        return res
