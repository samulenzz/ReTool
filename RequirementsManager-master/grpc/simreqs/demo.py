import time

from simreqs.similarity import reqs_similarity


DEMO_FRS = [
    {
        'event': '无条件',
        'agent': '数据导出',
        'operation': '为Word格式的文档',
        'input': '当前框架项目的整体数据导出为Word格式的',
        'output': '无输出',
        'restriction': '无约束',
    },
    {
        'event': '无条件',
        'agent': '系统',
        'operation': '够将评估结果输出到文档中',
        'input': '',
        'output': 'Word形式的评估报告',
        'restriction': '以所见即所得的方式',
    },
    {
        'event': '无条件',
        'agent': '导出数据子功能',
        'operation': '将当前项目导出为XML文件或者ZIP文件',
        'input': '当前项目导出为XML文件或者ZIP',
        'output': '无输出',
        'restriction': '无约束',
    }
]

DEMO_NFRS = [
    {
        'vtype': '用户页面响应时间一般',
        'rtype': '0',
        'sign': '小于等于',
        'value': '3',
        'unit': '秒',
    },
    {
        'vtype': '客户使用时界面的反应时间通常',
        'rtype': '0',
        'sign': '小于等于',
        'value': '3',
        'unit': '秒',
    },
    {
        'vtype': '打开模型数小于150个的项目的时间',
        'rtype': '0',
        'sign': '小于',
        'value': '3',
        'unit': '秒',
    },
    {
        'vtype': '能力评估分析工具构建评估指标体系可支持的层数',
        'rtype': '0',
        'sign': '大于等于',
        'value': '10',
        'unit': '层',
    }
]

DEMO_RRS = [
    {
        'vtype': '正常负载情况下系统正常运行',
        'sign1': '大于',
        'duration': '24小时',
        'sign2': '大于',
        'pr': '99.9%'
    },
    {
        'vtype': '正常负载情况下系统正常运行',
        'sign1': '大于',
        'duration': '24小时',
        'sign2': '小于',
        'pr': '50.9%'
    },
    {
        'vtype': '系统崩溃后恢复正常的时间',
        'sign1': '小于',
        'duration': '10分钟',
        'sign2': '等于',
        'pr': '100%'
    }
]


def run_demo():
    print(f'TimeStamp: {time.time()}')
    for i in range(len(DEMO_FRS)):
        for j in range(i + 1, len(DEMO_FRS)):
            similarity = reqs_similarity(DEMO_FRS[i], DEMO_FRS[j], 'FR')
            print(f'*************************************')
            print(DEMO_FRS[i])
            print(DEMO_FRS[j])
            print(f'Similarity: {similarity}')
    print(f'TimeStamp: {time.time()}')
    for i in range(len(DEMO_NFRS)):
        for j in range(i + 1, len(DEMO_NFRS)):
            similarity = reqs_similarity(DEMO_NFRS[i], DEMO_NFRS[j], 'NFR')
            print(f'*************************************')
            print(DEMO_NFRS[i])
            print(DEMO_NFRS[j])
            print(f'Similarity: {similarity}')
    print(f'TimeStamp: {time.time()}')
    for i in range(len(DEMO_RRS)):
        for j in range(i + 1, len(DEMO_RRS)):
            similarity = reqs_similarity(DEMO_RRS[i], DEMO_RRS[j], 'RR')
            print(f'*************************************')
            print(DEMO_RRS[i])
            print(DEMO_RRS[j])
            print(f'Similarity: {similarity}')
    print(f'TimeStamp: {time.time()}')
