from typing import List, Dict
import os.path as op

import jieba
from gensim.models import Word2Vec


STOPWORDS_PATH = op.join(op.dirname(__file__), 'data', 'stopwords_zh.txt')
STOPWORDS = {}
with open(STOPWORDS_PATH, encoding='utf-8') as f:
    stopwords = f.read().split('\n')
    STOPWORDS = {word: word for word in stopwords}

MODEL_PATH = op.join(op.dirname(__file__), '..', 'models', '20200326', 'word2vec.model')
MODEL = Word2Vec.load(MODEL_PATH)
MODEL.wv.init_sims(replace=True)


def _pre_process_sentence(sentence: str,
                          stopwords: Dict = None) -> List[str]:
    words = jieba.cut(sentence)
    if stopwords:
        words = [word for word in words if word not in stopwords]
    return words


def sentence_similarity(sentence1: str,
                        sentence2: str) -> int:
    words1 = _pre_process_sentence(sentence1, STOPWORDS)
    words2 = _pre_process_sentence(sentence2, STOPWORDS)

    # 移除不在语料库中的
    words1 = [word for word in words1 if word in MODEL.wv]
    words2 = [word for word in words2 if word in MODEL.wv]
    try:
        similarity = MODEL.wv.n_similarity(words1, words2)
    except Exception:
        similarity = None
    return similarity


# 需求结构化模板，value为权重
STRUCTURED_REQS_SCHEMA = {
    # 功能需求
    'FR': {
        'event': 1,
        'agent': 1,
        'operation': 1,
        'input': 1,
        'output': 1,
        'restriction': 1,
    },
    # 性能需求
    'NFR': {
        'vtype': 5,
        'rtype': 1,
        'sign': 1,
        'value': 0,
        'unit': 1,
    },
    # 可靠性需求
    'RR': {
        'vtype': 5,
        'sign1': 1,
        'duration': 1,
        'sign2': 1,
        'pr': 0,
    }
}

THRESHOLD = 0.78


def reqs_similarity(req1: Dict[str, str],
                    req2: Dict[str, str],
                    _type: str) -> float:
    assert _type in STRUCTURED_REQS_SCHEMA
    schema = STRUCTURED_REQS_SCHEMA[_type]

    product = 1
    sum_weight = 0
    for field in schema:
        str1 = req1[field]
        str2 = req2[field]
        if str1 and str2:
            sim = sentence_similarity(str1, str2)
        if sim:
            weight = schema[field]
            product *= (sim ** weight)
            sum_weight += weight

    return product ** (1/sum_weight)


def is_reqs_similar(req1: Dict[str, str],
                    req2: Dict[str, str],
                    _type: str) -> bool:
    similarity = reqs_similarity(req1, req2, _type)
    return similarity >= THRESHOLD
