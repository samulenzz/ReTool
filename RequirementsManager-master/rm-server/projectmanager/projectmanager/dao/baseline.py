from dataclasses import dataclass, field
from datetime import datetime
from typing import List

from pymongo.collection import Collection

from projectmanager.utils.uuid import generate_uuid


@dataclass
class BaselineNode:
    name: str  # 标题
    description: str  # 补充描述信息
    author: str  # 操作用户名
    created_time: str = None  # 创建的时间戳
    version: str = None

    def __post_init__(self):
        if not self.created_time:
            self.created_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        if not self.version:
            self.version = generate_uuid()

    def jsonify(self):
        return {
            'name': self.name,
            'description': self.description,
            'author': self.author,
            'created_time': self.created_time,
            'version': self.version,
        }


@dataclass
class Baseline:
    project_id: str  # 这里使用项目id作为基线的id
    nodes: List[BaselineNode] = field(default_factory=list)

    def jsonify(self):
        return {
            '_id': self.project_id,
            'nodes': [node.jsonify() for node in self.nodes]
        }


class BaselineDao:
    # 初始化基线
    def create(self, project):
        pass

    # 删除基线
    def delete(self, _id: str):
        pass

    # 添加节点
    def add_node(self, _id: str, node: BaselineNode):
        pass

    # 获取节点
    def get_node(self, _id: str, version: str) -> BaselineNode:
        pass

    # 获取基线内所有节点
    def get_all_nodes(self, _id: str) -> List[BaselineNode]:
        pass


class BaselineMongoDBDao(BaselineDao):
    def __init__(self, collection: Collection):
        self.collection = collection

    def create(self, project_id: str):
        baseline = Baseline(project_id)
        self.collection.insert_one(baseline.jsonify())

    def delete(self, project_id: str):
        self.collection.delete_one({'_id': project_id})

    def add_node(self, project_id: str, node: BaselineNode):
        baseline = self.collection.find_one({'_id': project_id})
        nodes = baseline['nodes']
        nodes.append(node.jsonify())
        new_nodes = {"$set": {'nodes': nodes}}
        self.collection.update({'_id': project_id}, new_nodes)

    def get_node(self, project_id: str, version: str) -> BaselineNode:
        baseline = self.collection.find_one({'_id': project_id})
        nodes = baseline['nodes']
        for node in nodes:
            if node['version'] == version:
                return BaselineNode(**node)
        return None

    def get_all_nodes(self, project_id: str) -> List[BaselineNode]:
        baseline = self.collection.find_one({'_id': project_id})
        nodes = baseline['nodes']
        return [BaselineNode(**node) for node in nodes]
