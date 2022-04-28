import json

strong = {
    'NF':  ['性能','响应','延迟','带宽','吞吐','负载','工作量','占用','内存','容量','等待','速度','利用率','功耗','加速',
            '并发','及时','准时'],
    'Rel': ['可靠','稳定','正确性','完备','容错','误差','恢复','故障','失效','失误','崩溃','异常','报错','丢失率'],
    'Sec': ['安全','机密','保密','密码','加密','解密','密钥','访问','控制','访问控制','权限','身份','验证','认证','防护',
            '入侵','病毒','恶意','后门','防火墙','口令','攻击','抵抗','泄露','非法','合法','可信','信任','保护','保障','指纹'],
}
weak = {
    'NF':  ['反应','反应时间','空间','等待时间','吞吐量','吞吐率','计算能力','执行','速度','执行速度','快速','延时','传输延迟',
            '通过延迟','工作负载','工作负荷','负荷','资源','利用','运用','使用率','存储','准确度','准确','精度','精准','准确性',
            '准确率','效率','高效','推迟','次','同时','同步'],
    'Rel': ['安全性','存取','存取控制','身份验证','身份认证','鉴别','认定','识别','锁定','抵御','隔离','窃取','限制'],
    'Sec': ['完整','一致','稠度','相容','相合','有效','整体','健全','检查','成熟','容错性','复原','合规','故障率','误失','误失率',
            '致命','关键','关键失效','关键错误','错误','严重','程度','预测','缺失','缺失率','损失','遗失','损失率','遗失率'],
}
strong_num = [len(strong['NF']), len(strong['Rel']), len(strong['Sec'])]
weak_num = [len(weak['NF']), len(weak['Rel']), len(weak['Sec'])]

def classify(json_reqs: str):
    result = []
    reqs = json.loads(json_reqs)['items']
    for req in reqs:
        result.append({'id': req['id'], 'type': _judge(req['description'])})
    return json.dumps({'item': result}, ensure_ascii=False)


def _judge(req: str) -> str:
    num = [0, 0, 0]
    label = {0: '3', 1: '4', 2: '7'}

    for i, kind in enumerate(['NF', 'Rel', 'Sec']):
        l = strong[kind]
        for word in l:
            if req.find(word) >= 0:
                num[i] += 1
    num = [n*n/strong_num[i] for i, n in enumerate(num)]
    if sum(num) != 0:
        return label[num.index(max(num))]

    num = [0, 0, 0]
    for i, kind in enumerate(['NF', 'Rel', 'Sec']):
        l = weak[kind]
        for word in l:
            if req.find(word) >= 0:
                num[i] += 1
    num = [n*n/weak_num[i] for i, n in enumerate(num)]
    if max(num) < 0.08:
        return '2'
    return label[num.index(max(num))]
