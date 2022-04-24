# encoding: utf-8
import json
import csv
import sys
import threading
from queue import Queue

from crawler_config import res_path, app_names, parse_res_path

# reload(sys)
# sys.setdefaultencoding('utf-8')

# app_names = ['Faceu+Android_com.lemon.faceu']
# ['优酷视频', '360手机卫士', '360手机桌面', '360云盘', '嘀嘀打车+Android_com.sdu.didi.psnger', # '作业帮+Android_com.baidu.homework']

# ['淘宝网', '美图秀秀', '今日头条+Android_com.ss.android.article.news','手机支付宝客户端', '微信android']


# 需要记录的信息示例:
# "create_time": "2016-06-24 23:36:28",
# "version_name": "2.1.3",
# "content": "如果屏幕可以长亮就可以了",
# "type": "good"


def parse_comment(app_name):
    file_object = open(res_path + app_name + '.txt', 'rb')
    csvfile = open(parse_res_path + app_name + '.csv', 'w', newline='')

    writer = csv.writer(csvfile)

    line_num = 0
    for line in file_object:
        line_num += 1
        comment = line.decode('utf-8')
        print('type: {}, last: {}'.format(type(comment), ord(comment[-1])))
        # try:
        line_json = json.loads(comment)
        # except BaseException as e:
        #     print('Error at line {}, reason:{}'.format(line_num, e))

        line_msgs = line_json['data']['messages']

        for msg in line_msgs:
            create_time = msg['create_time']
            version_name = msg['version_name']
            content = msg['content']
            msgtype = msg['type']

            # csv format
            try:
                writer.writerow([create_time, version_name, content, msgtype])
            except BaseException as e:
                print(e)

    csvfile.close()
    file_object.close()


queue = Queue()


class ThreadUrl(threading.Thread):
    def __init__(self, queue):
        threading.Thread.__init__(self)
        self.queue = queue

    def run(self):
        while True:
            app_name = self.queue.get()
            parse_comment(app_name)
            self.queue.task_done()


def main():
    for _ in range(len(app_names)):
        t = ThreadUrl(queue)
        t.setDaemon(True)
        t.start()

    for app_name in app_names:
        queue.put(app_name)

    queue.join()


if __name__ == '__main__':
    main()
