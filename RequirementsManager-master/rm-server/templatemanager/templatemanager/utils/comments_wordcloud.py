# -*- coding: utf-8 -*-
import jieba
import pandas as pd
import wordcloud
import platform
import base64
from typing import List

from templatemanager.utils.preprocess import filter_stop_words, jieba_cut_comment

# 黑体
_macos_font_path = '/System/Library/Fonts/STHeiti Medium.ttc'
# 黑体
_windows_font_path = 'C:\\Windows\\Fonts\\simhei.ttf'

_temp_wordcloud_png_file_name = './static/temp_wordcloud_png_file.png'


def _list2wordcloud(comments_list: list):
    if platform.system() == "Windows":
        font_path = _windows_font_path
    elif platform.system() == "Darwin":
        font_path = _macos_font_path
    else:
        print("unsupport platform")
        font_path = None
    # prepare the word list
    words = []
    for comment in comments_list:
        words += filter_stop_words(jieba_cut_comment(comment))
    # construct a new WordCloud with some specific configuration
    w = wordcloud.WordCloud(background_color=None, mode="RGBA", width=600, height=300,
                            font_path=font_path, max_words=120, collocations=False)
    # filter the stop words
    # generate
    w.generate(' '.join(words))
    w.to_file(_temp_wordcloud_png_file_name)
    return True


def png2base64(file_name):
    img = open(file_name, 'rb')
    img_read = img.read()
    img.close()
    return base64.b64encode(img_read).decode('utf-8')


def generateWordCloudBase64(file):
    # parse the df to list
    df = pd.read_csv(file, encoding='utf-8')
    # use the list to generate wordcloud picture

    if 'class' in df.columns:
        df = df[lambda x: x['class'] != 'best']

    # print(df.shape)
    # print(df.head())

    _list2wordcloud(df['comments'].to_list())

    return png2base64(_temp_wordcloud_png_file_name)


if __name__ == '__main__':
    comments = ['你好我好大家好',
                'wordcloud 库把词云当作一个WordCloud对象',
                '基本使用',
                '以WordCloud对象为基础，配置参数、加载文本、输出文件']
    res = _list2wordcloud(comments)
    # 400 * 200, about 56KB
    print(png2base64(_temp_wordcloud_png_file_name))
