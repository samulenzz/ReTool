from templatemanager.utils.preprocess import get_similarity
from templatemanager.utils.uuid import generate_uuid
from queue import PriorityQueue, Queue

from typing import Set, List, Dict

import time


def cluster_by_similarity(commentsDictList: List):
    comments = [x['comment'] for x in commentsDictList]
    commentsPQ = {}
    for comment in comments:
        commentsPQ.setdefault(comment, PriorityQueue())
    for i in range(len(comments)):
        c1 = comments[i]
        for j in range(i + 1, len(comments)):
            c2 = comments[j]
            sim = get_similarity(c1, c2)
            if sim > 0.8:
                commentsPQ[c1].put((1 - sim, c2))
                commentsPQ[c2].put((1 - sim, c1))

    graph: Dict = dict()
    for comment in comments:
        graph.setdefault(comment, set())
    for c1 in commentsPQ.keys():
        if not commentsPQ[c1].empty():
            _, c2 = commentsPQ[c1].get()
            graph[c1].add(c2)
            graph[c2].add(c1)
    remain = set(comments)
    res: List[Set] = []
    que = Queue()
    while len(remain) > 0:
        que.put(remain.pop())
        s: Set = set()
        while not que.empty():
            c1 = que.get()
            s.add(c1)
            for c2 in graph[c1]:
                if c2 in remain:
                    remain.remove(c2)
                    que.put(c2)
        res.append(s)

    comments2type = []
    type_index = 1
    for s in res:
        head = s.pop()
        if len(s) > 0:
            children = []
            for comment in s:
                children.append({
                    'comment': comment,
                    'problem': type_index
                })
            comments2type.append({
                'comment': head,
                'problem': type_index,
                'children': children
            })
        else:
            comments2type.append({
                'comment': head,
                'problem': type_index
            })
        type_index += 1
    # for s in res:
    #     for comment in s:
    #         comments2type.append({
    #             'comment': comment,
    #             'problem': type_index
    #         })
    #         # comments2type[comment] = type_index
    #     type_index += 1
    return comments2type

# if __name__ == '__main__':
#     comments = [
#         '太占地方？1G多',
#         '好用，就是内存，资讯多，同時建议下360',
#         '百度 越来内容越多打开越来越慢，最后抛弃你的会越来越多。',
#         '占用空间太大。',
#         '占用空间太大',
#         '干扰项，让我康康这能不能分对'
#     ]
#     # comments = [
#     #     '什么妲己你又弄那么多广告，我tmd看广告的奖励对不对，他妈却让我下了这个破百度，百度这个垃圾。这个破百度有啥用，你看吧，你手机里肯定会安装一个系统的流量管理器，要你这个百度有毛用就把科目二取消了，垃圾应用。',
#     #     '广告一堆',
#     #     '流氓软件垃圾软件，老子根本就没有打算下，直接广告推送，点到了，取消也取消不了，垃圾东西',
#     #     '百度怎么也开始耍流氓了？动不动审核就没有原因不通过。太他妈恶心人了，浪费时间等于浪费生命。',
#     #     '百度的视频不是一点点恶心，广告经常点不出来',
#     #     '垃圾，每次一点开广场舞的视频就自己播放了，我把手机一打开都是百度广告，删了',
#     #     '一星都不想给，百毒太恶心了，系统无故把我3年的贴吧账号封号了，说是违反了，那你有种把哪个帖子违反了发出来啊！不给原因就强制删除。而且申诉还要强制下载这个百毒的app，不下就不给申诉，真t嘛垃圾恶心。',
#     #     '你查个英语会给你标出音乐符号来随便一下都是什么广告，还有木马软件。',
#     #     '垃圾百度，每次打开都要弹出广告！！！',
#     #     '总是跳转支付宝，一直弹窗让你下载东西！垃圾软件！早就想卸载了',
#     #     '还不如以前，广告多，搜索不好用',
#     #     '广告越来越多了，文章页面有广告就算了，回答页面有广告我也忍了。但为什么刚进去就有广告？为什么有这么多广告还说无广告？360竟然开始骗人了，几个意思？',
#     #     '越来越不人性化了，看视频锁住我拉通知栏结果标题和作者都显现了，我点屏幕还不能收回去，往下滑直接就下个视频了，搜索引擎也是，最上面搞什么热点新闻，真的很烦人',
#     #     '为什么我下载的软件都有病毒？'
#     # ]
#
#     # 相似的字符串归类的依据是
#     # 这一波字符串中与其最相似的字符串，这两个字符串属于同一类
#     commentsPQ = {}
#     for comment in comments:
#         commentsPQ.setdefault(comment, PriorityQueue())
#     for i in range(len(comments)):
#         c1 = comments[i]
#         for j in range(i + 1, len(comments)):
#             c2 = comments[j]
#             sim = get_similarity(c1, c2)
#             print("/*{}\n{}\n sim={}*/".format(c1, c2, sim))
#             if sim > 0.8:
#                 commentsPQ[c1].put((1 - sim, c2))
#                 commentsPQ[c2].put((1 - sim, c1))
#
#     graph: Dict = dict()
#     for comment in comments:
#         graph.setdefault(comment, set())
#     for c1 in commentsPQ.keys():
#         if not commentsPQ[c1].empty():
#             _, c2 = commentsPQ[c1].get()
#             graph[c1].add(c2)
#             graph[c2].add(c1)
#     print(graph)
#     remain = set(comments)
#     res: List[Set] = []
#     que = Queue()
#     while len(remain) > 0:
#         que.put(remain.pop())
#         s: Set = set()
#         while not que.empty():
#             c1 = que.get()
#             s.add(c1)
#             for c2 in graph[c1]:
#                 if c2 in remain:
#                     remain.remove(c2)
#                     que.put(c2)
#         res.append(s)
#
#     comments2type = {}
#     type_index = 0
#     for s in res:
#         for comment in s:
#             comments2type[comment] = type_index
#         type_index += 1
#     print(res)
#     print(comments2type)
#
#     # comments2type = {}
#     # type = 0
#     # for i in range(len(comments)):
#     #     c1 = comments[i]
#     #     if c1 not in comments2type.keys():
#     #         comments2type[c1] = type
#     #         type += 1
#     #     for j in range(i + 1, len(comments)):
#     #         c2 = comments[j]
#     #         sim = get_similarity(c1, c2)
#     #         print("/*{}\n{}\n sim={}*/".format(c1, c2, sim))
#     #         if sim >= 0.8:
#     #             comments2type[c2] = comments2type[c1]
#     #         else:
#     #             comments2type[c2] = type
#     #             type += 1
#     # print(comments2type)
