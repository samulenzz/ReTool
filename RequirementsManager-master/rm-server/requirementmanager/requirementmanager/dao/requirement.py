from dataclasses import dataclass

from pymongo.collection import Collection

from requirementmanager.utils.uuid import generate_uuid


@dataclass
class Requirement:
    project_id: str  # 所属的项目id
    name: str  # 需求名称
    description: str  # 需求描述
    _id: str = None
    _type: str = None  # 需求类型

    # 基本信息
    status: str = None  # 状态
    priority: str = None  # 优先级
    expected_start_time: str = None  # 预计开始时间
    expected_end_time: str = None  # 预计结束时间
    author: str = None  # 创建者
    created_time: str = None  # 创建时间
    last_modify_time: str = None  # 最后修改时间

    # 需求追踪
    track_code: str = None  # 追踪到的代码
    track_test: str = None  # 追踪到的测试用例
    track_people: str = None  # 追踪到的人员

    def __post_init__(self):
        if not self._id:
            self._id = generate_uuid()

    def jsonify(self):
        return {
            '_id': self._id,
            'project_id': self.project_id,
            'name': self.name,
            'description': self.description,
            '_type': self._type,
            'status': self.status,
            'priority': self.priority,
            'expected_start_time': self.expected_start_time,
            'expected_end_time': self.expected_end_time,
            'author': self.author,
            'created_time': self.created_time,
            'last_modify_time': self.last_modify_time,
            'track_code': self.track_code,
            'track_test': self.track_test,
            'track_people': self.track_people,
        }


class RequirementDao:
    def create(self, requirement: Requirement):
        pass

    def delete(self, _id: str):
        pass

    def edit(self, _id: str, **attributes):
        pass

    def get(self, _id: str) -> Requirement:
        pass


class RequirementMongoDBDao(RequirementDao):
    def __init__(self, collection: Collection):
        self.collection = collection

    def create(self, requirement: Requirement):
        self.collection.insert_one(requirement.jsonify())

    def delete(self, _id: str):
        self.collection.delete_one({'_id': _id})

    def edit(self, _id: str, **attributes):
        new_values = {'$set': attributes}
        self.collection.update_one({'_id': _id}, new_values)

    def get(self, _id: str) -> Requirement:
        requirement_dict = self.collection.find_one({'_id': _id})
        if requirement_dict:
            requirement = Requirement(**requirement_dict)
        else:
            requirement = None
        return requirement
