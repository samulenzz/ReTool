from dataclasses import dataclass
from typing import Dict, List

from pymongo.collection import Collection


# @dataclass
# class User:
#     username: str
#     password: str
#     system_role: str
#     email: str = None
#     phone_number: str = None

#     def jsonify(self) -> Dict:
#         return {
#             'username': self.username,
#             'password': self.password,
#             'system_role': self.system_role,
#             'email': self.email,
#             'phone_number': self.phone_number,
#         }

@dataclass
class Template:
    _id: str
    template_name: str
    introduction: str
    last_time: str
    outline: str

    def jsonify(self) -> Dict:
        return {
            '_id': self._id,
            'template_name': self.template_name,
            "introduction": self.introduction,
            "last_time": self.last_time,
            'outline': self.outline,
        }


class TemplateDao:
    def create_template(self, template: Template):
        pass

    def delete_template(self, template_name: str):
        pass

    def edit_template(self, template_name: str, attributes: Dict):
        pass

    def get_template(self, template_name: str) -> Template:
        pass

    def get_all_templates(self) -> List[Template]:
        pass


class TemplateMongoDBDao(TemplateDao):
    def __init__(self, collection: Collection):
        self.collection = collection

    def create_template(self, template: Template):
        self.collection.insert_one(template.jsonify())

    def delete_template(self, template_name: str):
        self.collection.delete_one({'template_name': template_name})

    def edit_template(self, template_name: str, attributes: Dict):
        new_values = {"$set": attributes}
        self.collection.update_one(
            {'template_name': template_name}, new_values)

    def get_template(self, template_name: str) -> Template:
        template_dict = self.collection.find_one(
            {'template_name': template_name}
        )
        if template_dict:
            # template_dict.pop('_id')
            template = Template(**template_dict)
        else:
            template = None
        return template
