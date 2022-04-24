import csv
import pandas as pd
import json
from typing import Dict
from collections import Counter
import warnings
import time
import numpy as np

from sklearn.model_selection import train_test_split, StratifiedKFold, KFold
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.multiclass import OneVsRestClassifier
from sklearn import tree, svm, metrics, ensemble
from sklearn.neural_network import MLPClassifier

from gensim.models import KeyedVectors

from crawler_config import label_list, label_table
from preprocess import filter_stop_words, jieba_cut_commment, parse_manual_label_to_training


# https://www.zhihu.com/question/35486862/answer/462683110
# https://zhuanlan.zhihu.com/p/41637556
# https://www.zhihu.com/question/271470776

# https://www.zhihu.com/question/299549788/answer/865021864
# https://www.zhihu.com/question/299549788

def print_metrics_data(y_test, y_pred, index):
    print('-*-*-*-*-*-*Round {}*-*-*-*-*-*-'.format(index))
    acc = metrics.accuracy_score(y_test, y_pred)
    print('Accuracy score: %f' % (acc))
    recall = metrics.recall_score(y_test, y_pred, average='micro')
    print('Micro Recall: %f' % (recall))
    prec = metrics.precision_score(y_test, y_pred, average='micro')
    print('Micro Precision: %f' % (prec))
    f1 = metrics.f1_score(y_test, y_pred, average="micro")
    print('Micro F1 score: %f' % (f1))
    return (acc, recall, prec, f1)


def save_result_to_csv(comments, y_test: pd.Series, y_pred: np.ndarray):
    result = comments.reset_index()
    # print(result)
    # print('result shape: {}'.format(result.shape))
    y_test = y_test.reset_index()
    y_pred = pd.DataFrame(y_pred)
    # print('y_test shape: {}'.format(y_test.shape))
    # print('y_pred shape: {}'.format(y_pred.shape))
    for i in range(17):
        result = pd.concat([result, y_test.loc[:, label_list[i]],
                            y_pred.loc[:, i]], axis=1)
    # print(result.shape)
    result.to_csv('test_and_predict.csv', index=False)


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
    # _wv_from_text.save_word2vec_format(
    #     'e:\\Tencent_AILab_ChineseEmbedding_2M.twv', binary=True)

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


def comments_embedding(comments: pd.Series) -> pd.DataFrame:
    comments = comments.map(
        lambda x: ' '.join(filter_stop_words(jieba_cut_commment(x)))
    )
    print('training_df shape: {}'.format(training_df))

    vect = TfidfVectorizer()
    # vect = CountVectorizer(stop_words='english')
    data_X = pd.DataFrame(
        vect.fit_transform(comments).toarray(),
        columns=vect.get_feature_names(),
    )
    print("data_X's shape is{}".format(data_X.shape))
    print("data_X columns: {}".format(data_X.columns.values.tolist()[:200]))
    return data_X


training_data_path = './data/comment_with_label.csv'

if __name__ == '__main__':
    start_time = time.time()
    warnings.filterwarnings("ignore")

    df = pd.read_csv(training_data_path, encoding='utf-8',
                     index_col='index')
    # df = clean_data(df)

    # header = ['comment', 'label']
    training_df = pd.DataFrame(df['comment']).astype(str)
    y_df = df.drop('comment', axis=1)
    # training_df['label'] = training_df['label'].map(label_table)
    print(training_df.shape)

    # embedding the comments from sentence to vector
    # data_X = comments_embedding(training_df['comment'])
    data_X = tencent_embedding(training_df['comment'])

    SPLIT_CNT = 10
    seeds = [753357, 1014 * 2 + 1024, 4096, 2048, 20480]
    num_model_seed = len(seeds)
    skf = KFold(n_splits=SPLIT_CNT, random_state=seeds[0], shuffle=True)
    # acc = [0] * SPLIT_CNT
    f1 = [0] * SPLIT_CNT
    recall = [0] * SPLIT_CNT
    prec = [0] * SPLIT_CNT

    for index, (train_index, test_index) in enumerate(skf.split(data_X, y_df)):
        # divide the training and testing set
        # X_train, X_test, y_train, y_test = train_test_split(data_X, y_df,
        #                                                     test_size=0.1)
        X_train, X_test = data_X.iloc[train_index], data_X.iloc[
            test_index]
        y_train, y_test = y_df.iloc[train_index], y_df.iloc[test_index]

        # init and train the model

        # model = ensemble.ExtraTreesClassifier()
        # Micro Recall: 0.470657
        # Micro Precision: 0.805444
        # Micro F1 score: 0.594119

        # model = ensemble.RandomForestClassifier()
        # # Micro Recall: 0.697804
        # # Micro Precision: 0.607658
        # # Micro F1 score: 0.649462

        # model = OneVsRestClassifier(svm.LinearSVC(class_weight='balanced'))
        # # Micro Recall: 0.685827
        # # Micro Precision: 0.608175
        # # Micro F1 score: 0.644501
        # # TF-IDF
        # # Micro Recall: 0.678386
        # # Micro Precision: 0.647801
        # # Micro F1 score: 0.662641

        # word2vec
        # model = OneVsRestClassifier(svm.LinearSVC(class_weight='balanced'))
        # Micro Recall: 0.577258
        # Micro Precision: 0.683481
        # Micro F1 score: 0.625681

        # kernel: {'linear', 'poly', 'rbf', 'sigmoid', 'precomputed'},
        # model = OneVsRestClassifier(
        #     svm.SVC(kernel='linear', class_weight='balanced'))
        # Micro Recall: 0.697804
        # Micro Precision: 0.607658
        # Micro F1 score: 0.649462

        # model = tree.DecisionTreeClassifier()

        # model = tree.DecisionTreeClassifier(class_weight='balanced')
        # # Micro Recall: 0.519417
        # # Micro Precision: 0.505276
        # # Micro F1 score: 0.512005
        layer_sizes = (200, 200)
        model = MLPClassifier(hidden_layer_sizes=layer_sizes)
        # # Micro Recall: 0.586343
        # # Micro Precision: 0.692663
        # # Micro F1 score: 0.634916
        # word2vec
        # # Micro Recall: 0.608121
        # # Micro Precision: 0.716806
        # # Micro F1 score: 0.657740

        model.fit(X_train, y_train)

        # # get prediction
        y_pred = model.predict(X_test)

        cal = print_metrics_data(y_test, y_pred, index)
        # acc[index] = cal[0]
        recall[index] = cal[1]
        prec[index] = cal[2]
        f1[index] = cal[3]

    print('-*-*-*-*-*-*Average*-*-*-*-*-*-')
    # print('Accuracy score: %f' % (np.mean(acc)))
    print('Micro Recall: %f' % (np.mean(recall)))
    print('Micro Precision: %f' % (np.mean(prec)))
    print('Micro F1 score: %f' % (np.mean(f1)))

    # # save the result to csv
    # save_result_to_csv(df.loc[list(X_test.index.values), 'comment'],
    #                    y_test,
    #                    y_pred)
    print(time.time() - start_time)
