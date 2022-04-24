from templatemanager.mongodb import template_collection, document_collection


if __name__ == '__main__':
    # template_collection.drop()
    document_collection.drop()
    # print(document_collection.find_one(
    #     {'_id': '704e8f4ca4d511eb85aee442a68cda74'}))
    # print(list(document_collection.find()))
