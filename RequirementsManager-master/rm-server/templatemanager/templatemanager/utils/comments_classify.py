import pickle
import numpy as np
import pandas as pd
from sklearn.neural_network import MLPClassifier
from typing import List, Dict

from templatemanager.utils.preprocess import tencent_embedding

label_table = {'additional_cost': 0,  # 额外开销  功能0
               'functional_complaint': 1,  # 功能问题  功能0
               'compatibility_issue': 2,  # 兼容问题  可靠3
               'crashing': 3,  # 崩溃     可靠3
               'feature_removal': 4,  # 特性移除  功能0
               'feature_request': 5,  # 增加特性  功能0
               'network_problem': 6,  # 网络问题  可靠3
               'privacy_and_ethical_issue': 7,  # 隐私道德  安全2
               'resource_heavy': 8,  # 资源占用  性能1
               'response_time': 9,  # 响应时间  性能1
               'user_interface': 10,  # 界面交互  易用4
               'safety': 11,  # 财产安全  安全2
               'installation_issue': 12,  # 安装问题  可靠3
               'traffic_wasting': 13,  # 流量浪费  性能1
               'content': 14,  # 内容抱怨  易用4
               'update_issue': 15,  # 更新问题  可靠3
               'other': 16}  # 其他

label2chinese = {
    'additional_cost': '额外开销',  # 额外开销  功能0
    'functional_complaint': '功能问题',  # 功能问题  功能0
    'compatibility_issue': '兼容问题',  # 兼容问题  可靠3
    'crashing': '崩溃',  # 崩溃     可靠3
    'feature_removal': '特性移除',  # 特性移除  功能0
    'feature_request': '增加特性',  # 增加特性  功能0
    'network_problem': '网络问题',  # 网络问题  可靠3
    'privacy_and_ethical_issue': '隐私道德',  # 隐私道德  安全2
    'resource_heavy': '资源占用',  # 资源占用  性能1
    'response_time': '响应时间',  # 响应时间  性能1
    'user_interface': '界面交互',  # 界面交互  易用4
    'safety': '财产安全',  # 财产安全  安全2
    'installation_issue': '安装问题',  # 安装问题  可靠3
    'traffic_wasting': '流量浪费',  # 流量浪费  性能1
    'content': '内容抱怨',  # 内容抱怨  易用4
    'update_issue': '更新问题',  # 更新问题  可靠3
    'other': '16'}  # 其他

# 功能 0 1 4 5
# 性能 8 9 13
# 安全 7 11
# 可靠 2 3 6 12 15
# 易用 10 14
# [1, 0, 3, 3,
#   0, 0, 3, 2,
#   1, 1, 4, 2,
#   3, 1, 0, 3]

label_list = ['additional_cost', 'functional_complaint', 'compatibility_issue', 'crashing',
              'feature_removal', 'feature_request', 'network_problem', 'privacy_and_ethical_issue',
              'resource_heavy', 'response_time', 'user_interface', 'safety',
              'installation_issue', 'traffic_wasting', 'content', 'update_issue', 'other']

_model: MLPClassifier = None
_model_path = './static/MLP120_120.pkl'


def _mlp_pred(x_test):
    global _model
    if _model is None:
        with open(_model_path, 'rb') as f:
            _model = pickle.load(f)
    return _model.predict(x_test)


def _result2list(comments: pd.Series, y_pred: np.ndarray) -> Dict:
    aspect_list = ['功能', '性能', '安全', '可靠', '易用']
    label2aspect_index = [0, 0, 3, 3,
                          0, 0, 3, 2,
                          1, 1, 4, 2,
                          3, 1, 4, 3]
    res = dict()
    for aspect in aspect_list:
        res.setdefault(aspect, dict())
    for i in range(len(label2aspect_index)):
        label = label2chinese[label_list[i]]
        aspect = aspect_list[label2aspect_index[i]]
        res[aspect].setdefault(label, [])
    rows, cols = y_pred.shape
    for i in range(rows - 1):
        for j in range(cols - 1):
            if y_pred[i, j] == 1 and j < len(label2aspect_index):
                label = label2chinese[label_list[j]]
                aspect = aspect_list[label2aspect_index[j]]
                comment = comments[i]
                res[aspect][label].append({
                    'comment': comment,
                    'problem': 0
                })
    return res


def classify_comments(file):
    df = pd.read_csv(file, encoding='utf-8')
    if 'class' in df.columns:
        df = df[lambda x: x['class'] != 'best'].reset_index(drop=True)
    # print(df.shape)
    # print(df.head())

    x_test = tencent_embedding(df['comments'])
    y_pred = _mlp_pred(x_test)
    return _result2list(df['comments'], y_pred)
