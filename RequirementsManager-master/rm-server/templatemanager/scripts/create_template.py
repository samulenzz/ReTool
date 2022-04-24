from templatemanager.mongodb import template_collection
from templatemanager.dao.template import (
    Template, TemplateMongoDBDao,
    # SYSTEM_ROLE_SYSTEM_MANAGER, SYSTEM_ROLE_COMMON_USER
)
from templatemanager.dao.document import (
    Document, DocumentMongoDBDao
)

if __name__ == '__main__':
    template_collection.drop()

    import time

    template1 = Template(
        _id="test_id_1",
        template_name="example_template_1",
        introduction="introduction_1",
        last_time=time.asctime(time.localtime(time.time())),
        outline=["example_template_1_outline_1", "example_template_1_outline_2"],
    )
    template2 = Template(
        _id="test_id_2",
        template_name="example_template_2",
        introduction="introduction_2",
        last_time=time.asctime(time.localtime(time.time())),
        outline=["example_template_2_outline_1", "example_template_2_outline_2"],
    )

    template_mongodb_dao = TemplateMongoDBDao(template_collection)
    template_mongodb_dao.create_template(template1)
    template_mongodb_dao.create_template(template2)
