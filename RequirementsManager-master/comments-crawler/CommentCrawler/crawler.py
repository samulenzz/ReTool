# encoding: utf-8
import urllib.error
import urllib.parse
import urllib.request
from urllib.parse import quote
from queue import Queue
import threading
import json
import random
import time
import os

from crawler_config import LINE_BREAK, res_path, app_names, app_store_website

COUNT = 10

# COUNT = 10
# LINE_BREAK = '\n'
# res_path = './res/'

# app_names = [
#     # '360手机卫士',
#     'A.me+Android_com.ss.android.ugc.aweme',  # 抖音
#     '微信android',
#     '百度搜索'
# ]
# [ '美图秀秀'] # '淘宝网', , 'QQ邮箱+Android_com.tencent.androidqqmail', '今日头条+Android_com.ss.android.article.news',
#'高德地图+android', '手机支付宝客户端', '微信android', '酷狗音乐+android', '小米手环V1.0.0.08111+Android_com.xiaomi.hm.health',
# '安卓壁纸+android_com.androidesk']
# ['优酷视频','360手机卫士','360手机桌面','360云盘','嘀嘀打车+Android_com.sdu.didi.psnger','作业帮+Android_com.baidu.homework']
# print unquote(app_names[0])

# app_store_website = 'https://zhushou.360.cn/'


def download_comment(app_name):
    start = 0
    # change True into "total" condition
    total = 0x7FFFFFFF
    url_name = quote(app_name, '+')

    # print(url)

    user_agents = [
        'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11',
        'Opera/9.25 (Windows NT 5.1; U; en)',
        'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)',
        'Mozilla/5.0 (compatible; Konqueror/3.5; Linux) KHTML/3.5.5 (like Gecko) (Kubuntu)',
        'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.0.12) Gecko/20070731 Ubuntu/dapper-security Firefox/1.5.0.12',
        'Lynx/2.8.5rel.1 libwww-FM/2.14 SSL-MM/1.4.1 GNUTLS/1.2.9',
        "Mozilla/5.0 (X11; Linux i686) AppleWebKit/535.7 (KHTML, like Gecko) Ubuntu/11.04 Chromium/16.0.912.77 Chrome/16.0.912.77 Safari/535.7",
        "Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:10.0) Gecko/20100101 Firefox/10.0",
        'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.81 Safari/537.36 SE 2.X MetaSr 1.0'
    ]
    file_object = open(res_path + app_name + '.txt', 'w')

    comments_list = list()

    def write_file():
        print('app: {}, total: {}, start: {}'.format(
            app_name, total, start))
        file_object.write(LINE_BREAK.join(comments_list) + LINE_BREAK)
        comments_list.clear()
        time.sleep(random.uniform(4, 8))

    try:
        while start <= total // 5 and start <= 2000:
            url = 'https://comment.mobilem.360.cn/comment/getComments?baike={}&c=message&a=getmessage&start={}&count={}&type=&_=1616838858027'.format(
                url_name, start, COUNT)
            # don't encode '+', or there will be a mistake
            agent = random.choice(user_agents)

            headers = {'Referer': app_store_website,
                       'User-Agent': agent,
                       'Accept': '*/*'
                       }
            data = None

            request = urllib.request.Request(url, data, headers)
            response = urllib.request.urlopen(request)
            response_str = response.read()
            response_json = json.loads(response_str)

            # print response_str
            total = int(response_json['data']['total'])
            start += COUNT

            # file_object.write(str(response_str) + LINE_BREAK)
            comments_list.append(response_str.decode('utf-8'))

            if start % 100 == 0:
                write_file()
                # print('app: {}, total: {}, start: {}'.format(
                #     app_name, total, start))
                # file_object.write(LINE_BREAK.join(comments_list) + LINE_BREAK)
                # comments_list.clear()
                # # sleep_time = random.uniform(3, 7)
                # time.sleep(random.uniform(5, 15))

    finally:
        # file_object.write(LINE_BREAK.join(comments_list))
        if len(comments_list) > 0:
            write_file()
        file_object.close()


queue = Queue()


class ThreadUrl(threading.Thread):
    def __init__(self, queue):
        threading.Thread.__init__(self)
        self.queue = queue

    def run(self):
        # while True:
        try:
            app_name = self.queue.get()
            download_comment(app_name)
        except urllib.error.HTTPError as e:
            print(e)
        except urllib.error.URLError as e:
            print(e)
        # except urllib.socket.error as e:
        #     print (e.__weakref__)
        self.queue.task_done()


def main():
    if not os.path.exists(res_path):
        os.mkdir(res_path)

    for _ in range(len(app_names)):
        t = ThreadUrl(queue)
        t.setDaemon(True)
        t.start()

    for app_name in app_names:
        queue.put(app_name)

    queue.join()


if __name__ == '__main__':
    main()
