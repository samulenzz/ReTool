import json
import time

from requirementmanager.grpc_client.client import GrpcClient


grpc_client = GrpcClient()

_TYPE_MAP = {
    'FR': '2',
    'NFR': '3',
    'RR': '4',
}

_RTYPE_MAP = {
    '0': None,
    '1': '最大',
    '2': '最小',
    '3': '平均',
}

_SIGN_MAP = {
    '1': '小于',
    '2': '大于',
    '3': '等于',
    '4': '大于等于',
    '5': '小于等于',
    '6': '不等于',
}


def wrap_struct_req(raw_req):
    raw_req.pop('id')
    raw_req.pop('type')
    raw_req.pop('description')
    if 'groupid' in raw_req:
        raw_req.pop('groupid')
    if 'rtype' in raw_req:
        raw_req['rtype'] = _RTYPE_MAP[raw_req['rtype']]
    if 'sign' in raw_req:
        raw_req['sign'] = _SIGN_MAP[raw_req['sign']]
    if 'sign1' in raw_req:
        raw_req['sign1'] = _SIGN_MAP[raw_req['sign1']]
    if 'sign2' in raw_req:
        raw_req['sign2'] = _SIGN_MAP[raw_req['sign2']]
    return raw_req


def wrap_simreqs_data(data_path: str, opath: str):
    with open(data_path, encoding='utf-8') as f:
        raw_file = json.load(f)

    for _type, data in raw_file['data'].items():
        new_data = []

        for item in data:
            if not item['reqs'][0]:
                continue

            input_grpc = {
                'items': [
                    {'id': '0', 'name': '关键需求', 'description': item['reqs'][0], 'type': _TYPE_MAP[_type]},
                    {'id': '0', 'name': '关键需求', 'description': item['reqs'][1], 'type': _TYPE_MAP[_type]},
                ]
            }
            print(input_grpc)
            resp_grpc = grpc_client.structurization(json.dumps(input_grpc))
            resp_data = json.loads(resp_grpc)
            print(resp_data)
            struct_reqs = resp_data['items']

            struct_req1 = wrap_struct_req(struct_reqs[0]['result'][0])
            struct_req2 = wrap_struct_req(struct_reqs[1]['result'][0])
            new_data.append({'id': item['id'], 'reqs': [struct_req1, struct_req2]})

            time.sleep(1)

        raw_file['data'][_type] = new_data

    with open(opath, 'w', encoding='utf-8') as f:
        f.write(json.dumps(raw_file, indent=4, ensure_ascii=False))


def generate_nsimilar_reqs(data_path: str, opath: str):
    with open(data_path, encoding='utf-8') as f:
        raw_file = json.load(f)

    for _type, data in raw_file['data'].items():
        len_data = len(data)
        for i in range(0, len_data - 1, 3):
            tmp_req = data[i]['reqs'][1]
            data[i]['reqs'][1] = data[i+1]['reqs'][1]
            data[i+1]['reqs'][1] = data[i+2]['reqs'][1]
            data[i+2]['reqs'][1] = tmp_req

    with open(opath, 'w', encoding='utf-8') as f:
        f.write(json.dumps(raw_file, indent=4, ensure_ascii=False))


# wrap_simreqs_data('../../../simreqs/data/similar_reqs_raw.json', '../../../simreqs/data/similar_reqs_structured.json')

generate_nsimilar_reqs('../../../simreqs/data/similar_reqs_raw.json', '../../../simreqs/data/nsimilar_reqs_raw.json')
generate_nsimilar_reqs('../../../simreqs/data/similar_reqs_structured.json', '../../../simreqs/data/nsimilar_reqs_structured.json')
