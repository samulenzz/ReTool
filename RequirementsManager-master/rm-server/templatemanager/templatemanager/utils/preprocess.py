import numpy as np
import pandas as pd
from typing import List, Dict
import re
import jieba
from gensim.models import KeyedVectors
import time

stop_words_set = set()


def _load_stop_words_file(file_name):
    with open(file_name, 'r', encoding='utf-8') as stop_word_file:
        for line in stop_word_file:
            stop_words_set.add(line.rstrip())


def filter_stop_words(words: List) -> List:
    if len(stop_words_set) == 0:
        _load_stop_words_file('./static/哈工大停用词表.txt')

    def is_useful_word(word: str):
        s = word.strip()
        return len(s) > 0 and s not in stop_words_set and not re.match(r'(\d|\.)+(?!(\W))', s)

    return list(filter(is_useful_word, words))


def jieba_cut_comment(comment: str) -> List:
    # 判断一个unicode是否是汉字
    def is_chinese(uchar):
        return u'\u4e00' <= uchar <= u'\u9fa5'

    cut_result = []
    seg_list = jieba.lcut(comment)
    for seg in seg_list:
        seg = seg.lower()
        seg = re.sub(r'[\d_%]+', '', seg.strip())
        if not is_chinese(seg):
            continue
        cut_result.append(seg)
    return cut_result


_tencent_file = \
    'd:\\RequirementsManager2021\\comments-crawler\\tecent_ailab_word2vec\\Tencent_AILab_ChineseEmbedding_2M.twv'
_wv_from_text = None
_MAX_WORD_COUNT = 2000000  # // 10 * 9


def tencent_embedding(comments) -> pd.DataFrame:
    global _wv_from_text
    if _wv_from_text is None:
        start_time = time.time()
        print('-*-*-*-*-*-*Loading Word2Vec model*-*-*-*-*-*-')
        print('estimated time: {}'.format(13.6 / 1000000 * _MAX_WORD_COUNT))
        _wv_from_text = KeyedVectors.load_word2vec_format(
            _tencent_file, binary=True)
        _wv_from_text.init_sims(replace=True)
        print(
            '-*-*-*-*-*-*Finished, use {}*-*-*-*-*-*-'.format(time.time() - start_time))
    noword = set()

    def convert_word2vec(words: list):
        cnt = 0.0
        res = np.zeros(200)
        for word in words:
            try:
                res += _wv_from_text.get_vector(word)
                cnt += 1.0
            except Exception:
                noword.add(word)
        if cnt > 0:
            res = res / cnt
        return res

    data_X = list()
    for comment in comments:
        data_X.append(convert_word2vec(
            filter_stop_words(jieba_cut_comment(comment))))
    print('cannot find {} words, {}'.format(len(noword), list(noword)))
    data_X = pd.DataFrame(data_X)
    print(data_X.head())
    return data_X


def get_similarity(s1: str, s2: str):
    global _wv_from_text
    if _wv_from_text is None:
        start_time = time.time()
        _wv_from_text = KeyedVectors.load_word2vec_format(
            _tencent_file, binary=True)
        _wv_from_text.init_sims(replace=True)
        print(
            '-*-*-*-*-*-*Finished, use {}*-*-*-*-*-*-'.format(time.time() - start_time))

    def filter_word2vec(words: list):
        return list(filter(lambda x: _wv_from_text.has_index_for(x), words))

    w1 = filter_word2vec(filter_stop_words(jieba_cut_comment(s1)))
    w2 = filter_word2vec(filter_stop_words(jieba_cut_comment(s2)))
    return _wv_from_text.n_similarity(w1, w2)
