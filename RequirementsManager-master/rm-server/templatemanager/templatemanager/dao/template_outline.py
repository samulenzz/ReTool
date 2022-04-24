import json
from typing import List, Dict


class OutlineNode:
    _id: str
    father_id: str

    title: str
    children: List[str]

    def __init__(self, title):
        self.title = title
        self.children = []

    def jsonify(self):
        return {
            '_id': self._id,
            'father_id': self.father_id,
            "title": self.title,
            "children": self.children,
        }


class OutlineTree:
    root: OutlineNode
    children: List

    def __init__(self):
        pass

    def addNode(self):
        pass


if __name__ == '__main__':
    x = OutlineNode("1 综述")
    print(x.jsonify())
