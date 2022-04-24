import csv
import pandas as pd
import json
from typing import Dict
from collections import Counter
import warnings
import time
import numpy as np
import pickle

from sklearn.model_selection import train_test_split, StratifiedKFold, KFold
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.multiclass import OneVsRestClassifier
from sklearn import tree, svm, metrics, ensemble
from sklearn.neural_network import MLPClassifier

from gensim.models import KeyedVectors

from crawler_config import label_list, label_table
from preprocess import filter_stop_words, jieba_cut_commment, parse_manual_label_to_training


_tencent_file = '../tecent_ailab_word2vec/Tencent_AILab_ChineseEmbedding_2M.twv'
_wv_from_text = None
_MAX_WORD_COUNT = 2000000


def tencent_embedding(comments: pd.Series) -> pd.DataFrame:
    global _wv_from_text
    if _wv_from_text == None:
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
            filter_stop_words(jieba_cut_commment(comment))))
    print('cannot find {} words, {}'.format(len(noword), list(noword)))
    data_X = pd.DataFrame(data_X)
    print(data_X.head())
    return data_X


training_data_path = './data/comment_with_label.csv'

def save_model(path: str):
    start_time = time.time()
    warnings.filterwarnings("ignore")

    df = pd.read_csv(training_data_path, encoding='utf-8',
                     index_col='index')
    # df = clean_data(df)

    training_df = pd.DataFrame(df['comment']).astype(str)
    y_df = df.drop('comment', axis=1)
    print(training_df.shape)

    # embedding the comments from sentence to vector
    # data_X = comments_embedding(training_df['comment'])
    data_X = tencent_embedding(training_df['comment'])

    layer_sizes = (120, 120)
    model = MLPClassifier(hidden_layer_sizes=layer_sizes)

    model.fit(data_X, y_df)
    s = pickle.dumps(model)
    
    with open(path, 'wb') as f:
        f.write(s)
    print(time.time() - start_time)

if __name__ == '__main__':
    path = './MLP120_120.pkl'
    # save_model(path)
    model: MLPClassifier
    with open(path, 'rb') as f:
        model = pickle.load(f)
    # y_pred = model.predict()


def load_model():
    return None

def embedding(comments):
    model = load_model()

    for comment in comments:
        words = filter_stop_words(jieba_cut_commment(comment))
        cnt = 0.0
        res = np.zeros(200)
        for word in words:
            if word in model:
                res += model.get_vector(word)
                cnt += 1.0
        res = res / cnt if cnt > 0 else res 

    
