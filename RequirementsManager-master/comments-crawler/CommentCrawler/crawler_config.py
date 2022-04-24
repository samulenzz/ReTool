LINE_BREAK = '\n'

res_path = './res_txt/'

parse_res_path = './data/parseResults/'

low_review_path = './data/LowReviews/'

sample_reviews_path = './data/SampleReviews/'

cut_result_path = './data/cut_result/'

app_store_website = 'https://zhushou.360.cn/'

app_names = [
    '360手机卫士',
    'A.me+Android_com.ss.android.ugc.aweme',  # 抖音
    '微信android',
    '百度搜索',
    '拼多多+Android_com.xunmeng.pinduoduo',
    '手机支付宝客户端'
]

TYPE_BEST = 'best'
TYPE_GOOD = 'good'
TYPE_BAD = 'bad'

label_table = {'additional_cost': 0,
               'functional_complaint': 1,
               'compatibility_issue': 2,
               'crashing': 3,
               'feature_removal': 4,
               'feature_request': 5,
               'network_problem': 6,
               'privacy_and_ethical_issue': 7,
               'resource_heavy': 8,
               'response_time': 9,
               'user_interface': 10,
               'safety': 11,
               'installation_issue': 12,
               'traffic_wasting': 13,
               'content': 14,
               'update_issue': 15,
               'other': 16}

label_list = ['additional_cost', 'functional_complaint', 'compatibility_issue', 'crashing',
              'feature_removal', 'feature_request', 'network_problem', 'privacy_and_ethical_issue',
              'resource_heavy', 'response_time', 'user_interface', 'safety',
              'installation_issue', 'traffic_wasting', 'content', 'update_issue', 'other']

# additional_cost:              32      0.82%
# functional_complaint:         603     15.45%
# compatibility_issue:          81      2.08%
# crashing:                     584     14.97%
# feature_removal:              257     6.59%
# feature_request:              325     8.33%
# network_problem:              159     4.07%
# privacy_and_ethical_issue:    21      0.54%
# resource_heavy:               124     3.18%
# response_time:                190     4.87%
# user_interface:               50      1.28%
# safety:                       37      0.95%
# installation_issue:           45      1.15%
# traffic_wasting:              16      0.41%
# content:                      111     2.84%
# update_issue:                 692     17.73%
# other:                        1335    34.21%
# total:                        3902(4662)  100.00%(119.48%)
