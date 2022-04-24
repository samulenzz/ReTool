# import pprint
# from others import FRAndNFRRelation
# import json
#
# from UncertaintySpreadAnalyze.data import *
#
#
# def get_relationship_014(str1):  # 014 前提 依赖 交互
#
#     global result
#     global result_set
#
#     def check_append(R1, R2, kind):
#         if(R1['id'], R2['id'], kind) not in result_set:
#             result.append(
#                 {'id1': R1['id'], 'description1': R1['description'],
#                  'id2': R2['id'], 'description2': R2['description'],
#                  'relationType': str(kind)
#                  })
#             result_set.add((R1['id'], R2['id'], kind))
#
#     str2 = []
#     for i in str1:
#         str2.append(i)
#
#     for p in str1:
#         for q in str2:
#             if p['id'] == q['id']:
#                 continue
#             if (p['operation'] in q['event'] and p['operation'] != "") or (q['event'] in p['operation'] and q['event'] != ""):
#                 check_append(p, q, 0)
#                 check_append(q, p, 1)
#             if (p['output'] in q['input'] and p['output'] != "") or (q['input'] in p['output'] and q['input'] != ""):
#                 check_append(p, q, 4)
#
#     pprint.pprint(result)
#
# def get_relationship_4(str1):  # 4 交互
#
#     global result
#     global result_set
#
#     def check_append(R1, R2, kind):
#         if(R1['id'], R2['id'], kind) not in result_set:
#             result.append(
#                 {'id1': R1['id'],'id2': R2['id'],'relationType':'4'})
#             result_set.add((R1['id'], R2['id'], kind))
#     def check_overlap(str1:str,str2:str):
#         def rim(s:str):
#             return s.replace("[","").replace("]","").replace(" ","").lower()
#
#         if str1=="" or str1=="*" or str2=="" or str2=="*":
#             return False
#
#         l1=str1.split(", ")
#         l2=str2.split(", ")
#         s1=set()
#         s2=set()
#         for s in l1:
#             s=rim(s)
#             if s=="*":
#                 continue
#             s1.add(rim(s))
#         for s in l2:
#             s = rim(s)
#             if s == "*":
#                 continue
#             s2.add(rim(s))
#         if len(s1&s2)!=0:
#             return True
#         return False
#
#     str2 = []
#     for i in str1:
#         str2.append(i)
#
#     for p in str1:
#         for q in str2:
#             if p['id'] == q['id']:
#                 continue
#             # if (p['output'] in q['input'] and p['output'] != "") or (q['input'] in p['output'] and q['input'] != ""):
#             #     check_append(p, q, 4)
#             if check_overlap(p['output'],q['input']):
#                 check_append(p, q, 4)
#     print(len(result))
#     rela4out=r"C:\Users\wang9\Desktop\2\rela4_auto.json"
#     with open(rela4out,"w",encoding='UTF-8') as fout:
#         json.dump(result,fout)
#
# def get_relationship_56(str1, str2):  # 56 约束 实现
#     funData, nfunData = [], []
#     indexfunid, indexnfunid = [], []
#     for item in str1:
#         funData.append(item['description'])
#         indexfunid.append(item)
#     for item in str2:
#         nfunData.append(item['description'])
#         indexnfunid.append(item)
#
#     a = FRAndNFRRelation.getrequirement(funData, nfunData)
#     Result = a.GetRelatedFR_NFR
#
#     result = []
#
#     for r in Result:
#         temList = {
#             'id1': None, 'description1': None,
#             'id2': None, 'description2': None,
#             'relationType': '5'}
#         NewtemList = {
#             'id1': None, 'description1': None,
#             'id2': None, 'description2': None,
#             'relationType': '6'}
#
#         for i in indexnfunid:
#             if r[1] == i['description']:
#                 temList['id1'] = i['id']
#                 temList['description1'] = i['description']
#                 NewtemList['id2'] = i['id']
#                 NewtemList['description2'] = i['description']
#         for i in indexfunid:
#             if r[0] == i['description']:
#                 temList['id2'] = i['id']
#                 temList['description2'] = i['description']
#                 NewtemList['id1'] = i['id']
#                 NewtemList['description1'] = i['description']
#         if temList['id1'] is not None and temList['id2'] is not None:
#             result.append(temList)
#         if NewtemList['id1'] is not None and NewtemList['id2'] is not None:
#             result.append(NewtemList)
#
#     pprint.pprint(result)
#
#
# result, result_set = [], set()
# if __name__ == '__main__':
#     get_relationship_4(testF)
#     # 分析功能需求间的关系 (可分析 0前提 1依赖 4交互)
#     # get_relationship_014(testF)
#
#     # 分析功能需求和非功能需求间的关系 （可分析 5约束 6实现）
#     # get_relationship_56(CNfunction,testNf)
#
#     # 2包含 3细化 两种关联关系须借助文档结构人工标注