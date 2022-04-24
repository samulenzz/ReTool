from typing import List

from pymongo.collection import Collection

from templatemanager.dao.template import Template


class TemplateListDao:
    def get_all_templates(self) -> List[Template]:
        pass


class TemplateListMongoDBDao(TemplateListDao):
    def __init__(self, collection: Collection):
        self.collection = collection

    def get_all_templates(self) -> List[Template]:
        templates_list = self.collection.find()
        res = []
        for template_dict in templates_list:
            # template_dict.pop('_id')
            res.append(Template(**template_dict))
        return res
