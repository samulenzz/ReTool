# encoding: utf-8
from pprint import pprint
import csv
import random
import xlwt
import xlrd
import sys
import re
import jieba
import random
import pandas as pd

from typing import List, Dict

from crawler_config import app_names, parse_res_path, low_review_path, sample_reviews_path, cut_result_path, label_list, label_table, TYPE_GOOD, TYPE_BAD

import json


def jieba_cut_commment(comment: str) -> List:
    # 判断一个unicode是否是汉字
    def is_chinese(uchar):
        return uchar >= u'\u4e00' and uchar <= u'\u9fa5'
    cut_result = []
    seg_list = jieba.lcut(comment)
    for seg in seg_list:
        seg = seg.lower()
        seg = re.sub(r'[\d_%]+', '', seg.strip())
        if not is_chinese(seg):
            continue
        cut_result.append(seg)
    return cut_result


# 把评论转成arff格式,供后面WEKA API使用
def get_text_arff(words_list: List, arff_file):
    arff_file.write('@relation multiPre\r\n' +
                    '@attribute text string\r\n' +
                    '@attribute @@class@@ {all}\r\n' +
                    '@data\r\n')
    for content in words_list:
        arff_file.write('\'' + ' '.join(content) + '\',all\n')


stop_words_set = set()


def load_stop_words_file(file_name):
    with open(file_name, 'r', encoding='utf-8') as stop_word_file:
        for line in stop_word_file:
            stop_words_set.add(line.rstrip())
        # print(stop_words_set)


def filter_stop_words(words: List) -> List:
    if len(stop_words_set) == 0:
        load_stop_words_file('./data/哈工大停用词表.txt')

    def is_uselful_word(word: str):
        s = word.strip()
        return len(s) > 0 and s not in stop_words_set and not re.match(r'(\d|\.)+(?!(\W))', s)

    return list(filter(is_uselful_word, words))


arff_route = './parse_arff/'


def lda_test(corpus):
    from gensim.models import LdaModel
    from gensim.models.tfidfmodel import TfidfModel
    from gensim import corpora

    dictionary = corpora.Dictionary(corpus)
    dictionary.filter_extremes(no_below=3)
    dictionary.compactify()

    corpus = [dictionary.doc2bow(s) for s in corpus]
    corpora.MmCorpus.serialize('corpus_bow.mm', corpus)

    import logging
    logging.basicConfig(
        format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
    # Set training parameters.
    num_topics = 10
    chunksize = 2000
    passes = 20
    iterations = 400
    # Don't evaluate model perplexity, takes too much time.
    eval_every = None
    # Make a index to word dictionary.
    # temp = dictionary[0]  # This is only to "load" the dictionary.
    id2word = dictionary.id2token

    model = LdaModel(
        corpus=corpus,
        id2word=id2word,
        chunksize=chunksize,
        alpha='auto',
        eta='auto',
        iterations=iterations,
        num_topics=num_topics,
        passes=passes,
        eval_every=eval_every
    )
    top_topics = model.top_topics(corpus)  # , num_words=20)

    # Average topic coherence is the sum of topic coherences of all topics, divided by the number of topics.
    avg_topic_coherence = sum([t[1] for t in top_topics]) / num_topics
    print('Average topic coherence: %.4f.' % avg_topic_coherence)


def parse_manual_label_to_training(df: pd.DataFrame) -> pd.DataFrame:
    res_list = []
    for _, row in df.iterrows():
        comment = row['comment']
        for label in label_list:
            if not pd.isnull(row[label]):
                res_list.append({
                    'comment': str(comment),
                    'label': label
                })
                break
    return pd.DataFrame(res_list, columns=['comment', 'label'])


def get_label_count(df: pd.DataFrame) -> dict:
    res = dict()
    for label in label_list:
        res.setdefault(label, 0)
    for _, row in df.iterrows():
        for label in label_list:
            res[label] += row[label]
    return res


def clean_data(df):
    for index, row in df.iterrows():
        for label in label_list:
            if pd.isna(row[label]):
                df.at[index, label] = 0
            else:
                data = str(row[label]).strip()
                if len(data) > 0 and data[0] == '1':
                    df.at[index, label] = 1
                else:
                    df.at[index, label] = 0
    for label in label_list:
        df[label] = df[label].astype(int)
    return df


def get_training_data(df: pd.DataFrame) -> Dict:
    label2comments = dict()
    for label in label_list:
        label2comments.setdefault(label, list())
    for _, row in df.iterrows():
        comment = row['comment']
        for label in label_list:
            if not pd.isnull(row[label]):
                label2comments[label].append(comment)
    total = 0
    for label in label_list:
        total += len(label2comments[label])
        print("%s has %d comments" % (label, len(label2comments[label])))
    print('total %d comments classified' % (total))
    return label2comments


if __name__ == '__main__':
    df = pd.read_csv('./data/comment_with_label.csv',
                     encoding='utf-8',
                     index_col='index')
    label2cnt = get_label_count(df)
    total = df.shape[0]
    for label in label_list:
        print('{}: {} {:.2%}'.format(label,
                                     label2cnt[label],
                                     label2cnt[label] / total))

# if __name__ == '__main__':
#     cnt = 150 // len(app_names)
#     new_comment_list = []
#     for app in app_names:
#         f = open('{}{}.csv'.format(parse_res_path, app), 'r')
#         reader = csv.reader(f)
#         app_comment = []
#         i = 0
#         for _, _, comment, type in reader:
#             if type == TYPE_BAD or type == TYPE_GOOD:
#                 app_comment.append(comment)
#         f.close()
#         new_comment_list.extend(random.sample(app_comment, cnt))
#     df = pd.read_csv('./data/comment_with_label.csv', index_col='index')
#     for comment in new_comment_list:
#         line = dict()
#         line['comment'] = comment
#         for label in label_list:
#             line[label] = 0
#         df = df.append(line, ignore_index=True)
#     df.to_csv("new_comments_with_label.csv")

# if __name__ == '__main__':
#     # get stop words set
#     load_stop_words_file('./data/哈工大停用词表.txt')
#     # handle each APP's comments
#     for app_name in app_names:
#         with open('{}{}.csv'.format(parse_res_path, app_name), 'r') as f:
#             reader = csv.reader(f)

#             cut_result = []
#             # cut comments to word vector with jieba
#             for _, _, comment, _ in reader:
#                 jieba2word_list = jieba_cut_commment(comment)
#                 cut_result.append(filter_stop_words(jieba2word_list))

#             # print(cut_result[:min(len(cut_result), 5)])

#             cut_file = open('{}{}.txt'.format(cut_result_path, app_name), 'w')
#             cut_file.write(json.dumps(cut_result))
#             cut_file.close()

#             # dictionary = corpora.Dictionary(cut_result)
#             # corpus = [dictionary.doc2bow(text) for text in cut_result]
#             # tf_idf_model = TfidfModel(corpus, normalize=False)
#             # word_tf_tdf = list(tf_idf_model[corpus])
#             # print('词典:', dictionary.token2id)
#             # print('词频:', corpus)
#             # print('词的tf-idf值:', word_tf_tdf)
#             # # convert the jieba cutting result to `.arff` file
#             # arff_file = open('{}{}.arff'.format(arff_route, app_name), 'w')
#             # get_text_arff(cut_result, arff_file)
#             # arff_file.close()

#             # lda_test(cut_result)
