from dataclasses import dataclass, field
from typing import List, Dict

from pymongo.collection import Collection

from requirementmanager.utils.uuid import generate_uuid


REQUIREMENT_TYPE_MAP = {
    '2': '功能需求',
    '3': '性能需求',
    '4': '可靠性需求',
    '7': '安全性需求',
}


@dataclass
class RequirementTreeNode:
    _id: str  # 需求条目id
    name: str  # 该需求条目的名称
    father_id: str = None
    children_ids: List[str] = field(default_factory=list)

    def jsonify(self):
        return {
            '_id': self._id,
            'name': self.name,
            'father_id': self.father_id,
            'children_ids': self.children_ids,
        }


@dataclass
class RequirementTree:
    project_id: str  # 项目id
    _id: str = None  # uuid
    # 根节点，存储功能需求节点id.....
    root_nodes: List[str] = field(default_factory=list)
    # 需求条目节点
    requirement_nodes: Dict = field(default_factory=dict)

    def __post_init__(self):
        if not self._id:
            self._id = generate_uuid()
        if not self.root_nodes:
            for key, value in REQUIREMENT_TYPE_MAP.items():
                node = RequirementTreeNode(key, value)
                self.root_nodes.append(node._id)
                self.requirement_nodes[node._id] = node.jsonify()

    def jsonify(self):
        return {
            '_id': self._id,
            'project_id': self.project_id,
            'root_nodes': self.root_nodes,
            'requirement_nodes': self.requirement_nodes,
        }

    def add_node(self, node: RequirementTreeNode, base_id: str, location: str):
        # base_id是插入的位置的id，location为"inner", "before", "after"
        # 修改父节点
        # 如果是inner类型，则父节点就是base_id节点，否则是base_id的父id
        if location == 'inner':
            father_node = self.requirement_nodes[base_id]
            father_node['children_ids'].append(node._id)
        else:
            offset = 0 if location == 'before' else 1
            father_id = self.requirement_nodes[base_id]['father_id']
            father_node = self.requirement_nodes[father_id]
            for i, child_id in enumerate(father_node['children_ids'][:]):
                if child_id == base_id:
                    father_node['children_ids'].insert(i + offset, node._id)
        self.requirement_nodes[father_node['_id']] = father_node

        # 添加新节点
        node.father_id = father_node['_id']
        self.requirement_nodes[node._id] = node.jsonify()

    def delete_node(self, requirement_id: str):
        # 删除节点
        node = self.requirement_nodes.pop(requirement_id)
        # 修改父节点
        father_node = self.requirement_nodes[node['father_id']]
        father_node['children_ids'].remove(requirement_id)
        self.requirement_nodes[node['father_id']] = father_node

    def edit_node(self, requirement_id: str, base_id: str, location: str):
        # 删除节点，再添加节点
        node_dict = self.requirement_nodes[requirement_id]
        node = RequirementTreeNode(**node_dict)
        self.delete_node(requirement_id)
        self.add_node(node, base_id, location)

    def get_elementui_tree(self):
        """生成Element UI tree组件格式"""
        root_node = RequirementTreeNode(
            'root', 'root', children_ids=[key for key in REQUIREMENT_TYPE_MAP]
        )
        return self._get_children_node_recursively(root_node.jsonify())

    def _get_children_node_recursively(self, node: Dict):
        res = []
        for child_id in node['children_ids']:
            tmp_node_dict = self.requirement_nodes[child_id]
            res.append({
                '_id': tmp_node_dict['_id'],
                'label': tmp_node_dict['name'],
                'children': self._get_children_node_recursively(tmp_node_dict)
            })
        return res

    def get_node_type(self, node_id: str):
        while True:
            if node_id in [key for key in REQUIREMENT_TYPE_MAP]:
                return node_id
            node_id = self.requirement_nodes[node_id]['father_id']

    def get_children_ids(self, node_id: str):
        res = []
        node = self.requirement_nodes[node_id]
        for child_id in node['children_ids']:
            res.append(child_id)
            res += self.get_children_ids(child_id)
        return res


class RequirementTreeDao:
    def create(self, project_id: str):
        pass

    def delete(self, project_id: str):
        pass

    def edit(self, project_id: str, **attributes):
        pass

    def get(self, project_id: str) -> RequirementTree:
        pass

    def add_tree_node(self, project_id: str, new_node: RequirementTreeNode,
                      base_id: str, offset: str):
        pass

    def delete_tree_node(self, project_id: str, requirement_id: str):
        pass

    def edit_tree_node(self, project_id: str, requirement_id: str,
                       base_id: str, location: str):
        pass


class RequirementTreeMongoDBDao(RequirementTreeDao):
    def __init__(self, collection: Collection):
        self.collection = collection

    def create(self, tree: RequirementTree):
        self.collection.insert_one(tree.jsonify())

    def delete(self, project_id: str):
        self.collection.delete_one({'project_id': project_id})

    def edit(self, project_id: str, **attributes):
        new_values = {'$set': attributes}
        self.collection.update_one({'project_id': project_id}, new_values)

    def get(self, project_id: str) -> RequirementTree:
        tree_dict = self.collection.find_one({'project_id': project_id})
        if tree_dict:
            tree = RequirementTree(**tree_dict)
        else:
            tree = None
        return tree

    def add_tree_node(self, project_id: str, new_node: RequirementTreeNode,
                      base_id: str = None, location: str = None):
        tree = self.get(project_id)
        tree.add_node(new_node, base_id, location)
        self.edit(project_id, requirement_nodes=tree.requirement_nodes)

    def delete_tree_node(self, project_id: str, requirement_id: str):
        tree = self.get(project_id)
        tree.delete_node(requirement_id)
        self.edit(project_id, requirement_nodes=tree.requirement_nodes)

    def edit_tree_node(self, project_id: str, requirement_id: str,
                       base_id: str, location: str):
        tree = self.get(project_id)
        tree.edit_node(requirement_id, base_id, location)
        self.edit(project_id, requirement_nodes=tree.requirement_nodes)
