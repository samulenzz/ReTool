import os
import time
import json
import grpc
from concurrent import futures
from Proto import Requirement_pb2, Requirement_pb2_grpc

from core.Judge import is_conflict, input_output_condition
from core.Req import Req
from core.FReq import FReq
from core.NFReq import NFReq
from core.RelReq import RelReq
from core import RCD_NLP
from core import ReSplit, ReSuggRelate

from simreqs.similarity import is_reqs_similar


def split_sentence(text):
    req_list = []
    # for word in ['所示', '注：']:
    #     if word in text:
    #         return []
    s = ''.join(text.split())
    s = s[:-1] if s[-1] in ['。', '；'] else s
    # 停用词表
    words = ['并且', '或者', '而且', '可以', '只有', ]
    for word in words:
        text = text.replace(word, '')
    split_list = s.split('。')
    for s in split_list:
        for s0 in s.split('；'):
            if '所示' in s0 or '注：' in s0:
                continue
            if s0[0] == '并' or s0[0] == '而':
                s0 = s0[1:]
            req_list.append(s0 + '。')
    return req_list


class ModelServicer(Requirement_pb2_grpc.RequirementServicer):
    def structurization(self, request, context):
        type_dict = {'2': FReq, '3': NFReq, '4': RelReq}
        json_original = request.value
        reqs = json.loads(json_original)['items']
        groupid_count = 1
        Items = []

        for req in reqs:
            if req['type'] not in type_dict.keys():
                continue
            class_name = type_dict[req['type']]
            req_list = split_sentence(req['description'])
            if class_name == FReq and len(req_list) > 1:
                groupid = groupid_count
                groupid_count += 1
            else:
                groupid = 0
            result = []
            for r_text in req_list:
                if len(r_text) < 6:
                    continue
                r = class_name.parse_req(r_text)

                if r is None:
                    continue
                if class_name == FReq:
                    r.groupid = groupid
                d = {'id': req['id'], 'type': req['type'], 'description': r_text}
                result.append({**d, **r.__dict__})
            if len(result) == 0:
                continue
            result_dict = {'id': req['id'], 'result': result}
            Items.append(result_dict)

        Items_dict = {'items': Items}
        response = Requirement_pb2.Value()
        response.value = json.dumps(Items_dict, ensure_ascii=False)
        return response

    def conflictdetect(self, request, context):
        json_original = request.value
        reqs = json.loads(json_original)['items']
        Freqs = []          # List[Tuple[Req, str]]
        conflicts = []
        groupid_count = 1

        for req in reqs:
            if req['type'] == '2' or req['type'] == '7':
                req_list = split_sentence(req['description'])
                if len(req_list) > 0:
                    groupid = groupid_count
                    groupid_count += 1
                else:
                    groupid = 0
                for r_text in req_list:
                    try:
                        r = RCD_NLP.parse(r_text)
                    except BaseException:
                        continue
                    r.groupid = groupid
                    Freqs.append((r, r_text, req['id']))

        for i, r1_pair in enumerate(Freqs):
            for r2_pair in Freqs[i:]:
                r1, r2 = r1_pair[0], r2_pair[0]
                if r1.groupid == r2.groupid and r1_pair[1] == r2_pair[1] and r1.groupid != 0:
                    continue
                result = is_conflict(r1, r2)
                if len(result) > 0:
                    conflict_reqs = [ {'id': r1_pair[2], 'description': r1_pair[1]}, {'id': r2_pair[2], 'description': r2_pair[1]} ]
                    conflicts.append({'type': result[0], 'requirements': conflict_reqs})

        conflict_result = {'conflicts': conflicts}
        response = Requirement_pb2.Value()
        response.value = json.dumps(conflict_result, ensure_ascii=False)
        return response

    def relationship(self, request, context):
        json_original = request.value
        reqs = json.loads(json_original)['items']
        Freqs = []      # List[Tuple[Req, str]]
        result = []
        result_set = set()
        groupid_count = 1

        for req in reqs:
            if req['type'] == '2':
                req_list = split_sentence(req['description'])
                if len(req_list) > 0:
                    groupid = groupid_count
                    groupid_count += 1
                else:
                    groupid = 0
                for r_text in req_list:
                    try:
                        r = RCD_NLP.parse(r_text)
                    except BaseException:
                        continue
                    r.groupid = groupid
                    Freqs.append((r, r_text, req['id'], req['name']))

        for i, r1_pair in enumerate(Freqs):
            for r2_pair in Freqs[i+1:]:
                r1, r2 = r1_pair[0], r2_pair[0]
                if r1.groupid == r2.groupid or r1_pair[1] == r2_pair[1]:
                    continue
                if input_output_condition(r1, r2):
                    code = 'id1:{}__id2:{}__{}'.format(r1_pair[2], r2_pair[2], 4)
                    if code not in result_set:
                        result.append({'id1': r1_pair[2], 'description1': r1_pair[1], 'id2': r2_pair[2], 'description2': r2_pair[1], 'relationType': '4'})
                        result_set.add(code)
                if input_output_condition(r2, r1):
                    code = 'id1:{}__id2:{}__{}'.format(r2_pair[2], r1_pair[2], 4)
                    if code not in result_set:
                        result.append({'id1': r2_pair[2], 'description1': r2_pair[1], 'id2': r1_pair[2], 'description2': r1_pair[1], 'relationType': '4'})
                        result_set.add(code)
                index = r2_pair[1].find('完成后')
                if index > 0 and r2_pair[1][0:index] in r1_pair[3]:
                    code = 'id1:{}__id2:{}__{}'.format(r1_pair[2], r2_pair[2], 0)
                    if code not in result_set:
                        result_set.add(code)
                        result.append({'id1': r1_pair[2], 'description1': r1_pair[1], 'id2': r2_pair[2], 'description2': r2_pair[1], 'relationType': '0'})
        result = {'result': result}
        response = Requirement_pb2.Value()
        response.value = json.dumps(result, ensure_ascii=False)
        return response

    def Itemized(self, request, context):
        docData = json.loads(request.value)
        docDesc = docData['description']
        keyWord = docData['keyword']
        response = Requirement_pb2.ReValue()
        gr = ReSplit.getItemizedRequirement(docDesc, keyWord)
        result = {'id': docData['id'], "result": gr.splitRequirement()}
        resultJson = json.dumps(result, ensure_ascii=False)
        response.value1 = resultJson
        return response

    def Relate_Re_Sugg(self, request, context):
        docList = []
        suggList = []
        indexDocList = []
        indexSuggList = []
        docData = json.loads(request.value)['items']
        suggData = json.loads(request.value)['suggestions']
        for i in docData:
            docList.append(i['description'])
            indexDocList.append(i)
        for i in suggData:
            suggList.append(i['description'])
            indexSuggList.append(i)
        response = Requirement_pb2.ReValue()
        gr = ReSuggRelate.getrequirement(docList, suggList)
        resultRelatedRE_Sugg = gr.GetRelatedRE_Sugg()
        resultList = []
        for i in resultRelatedRE_Sugg:
            temList = {'itemid': None, 'sugesid': None, 'keyword': None}
            for j in indexDocList:
                if i[0] == j['description']:
                    temList['itemid'] = j['itemid']
            for n in indexSuggList:
                if i[1] == n['description']:
                    temList['sugesid'] = n['sugesid']
            temList['keyword'] = i[2]
            if temList['itemid'] is not None and temList['sugesid'] is not None and temList['keyword'] is not None:
                resultList.append(temList)
        result = {'items': resultList}
        ReaultJson = json.dumps(result, ensure_ascii=False)
        response.value1 = ReaultJson
        return response

    def similarity(self, request, context):
        # 先进行条目化
        response = self.structurization(request, context)
        items_dict = json.loads(response.value)
        items_list = []
        for i in items_dict['items']:
            for j in i['result']:
                items_list.append(j)

        # 需求进行归类
        reqs_dict = {
            'FR': [], 'NFR': [], 'RR': []
        }
        type_map = {
            '2': 'FR', '3': 'NFR', '4': 'RR'
        }
        for item in items_list:
            _type = type_map[item['type']]
            reqs_dict[_type].append(item)

        # 同一类别的需求，两两计算是否相似
        res_data = []
        sign_map = {'1': '小于', '2': '大于', '3': '等于', '4': '大于等于', '5': '小于等于', '6': '不等于'}
        for type_, reqs in reqs_dict.items():
            for i in range(len(reqs) - 1):
                for j in range(i + 1, len(reqs)):
                    req1 = reqs[i].copy()
                    req2 = reqs[j].copy()
                    # 将条目化后的数字转换回字符
                    if type_ == 'NFR':
                        req1['sign'] = sign_map[req1['sign']]
                        req2['sign'] = sign_map[req2['sign']]
                    elif type_ == 'RR':
                        req1['sign1'] = sign_map[req1['sign1']]
                        req1['sign2'] = sign_map[req1['sign2']]
                        req2['sign1'] = sign_map[req2['sign1']]
                        req2['sign2'] = sign_map[req2['sign2']]

                    # 判断是否相似，如果相似，添加至返回值
                    if is_reqs_similar(req1, req2, type_):
                    # if True:
                        res_data.append({
                            'req1': {
                                'id': req1['id'],
                                'description': req1['description']
                            },
                            'req2': {
                                'id': req2['id'],
                                'description': req2['description']
                            }
                        })

        # 返回值
        response = Requirement_pb2.Value()
        response.value = json.dumps(res_data, ensure_ascii=False)
        return response



Req.run()
CorNLP_path = os.getcwd() + os.sep + 'CoreNLP'   # CoreNLP目录
RCD_NLP.start(CorNLP_path)

server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
Requirement_pb2_grpc.add_RequirementServicer_to_server(ModelServicer(), server)
print('Starting server. Listening on port 50051.')
server.add_insecure_port('[::]:50051')
server.start()

# 添加睡眠循环以持续服务
try:
    while True:
        time.sleep(24 * 60 * 60)
except KeyboardInterrupt:
    server.stop(0)
    RCD_NLP.close()