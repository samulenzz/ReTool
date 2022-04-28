import json
import os.path as op

import numpy as np

from simreqs.similarity import (
    is_reqs_similar, _pre_process_sentence, THRESHOLD, STOPWORDS
)


def wordbag_similar(req1: str, req2: str):
    words1 = list(_pre_process_sentence(req1, STOPWORDS))
    words2 = list(_pre_process_sentence(req2, STOPWORDS))

    wordbag = list(set(words1 + words2))
    vec1 = np.zeros((len(wordbag)))
    vec2 = np.zeros((len(wordbag)))
    for word in words1:
        index = wordbag.index(word)
        vec1[index] += 1
    for word in words2:
        index = wordbag.index(word)
        vec2[index] += 1

    similarity = np.dot(vec1, vec2)/(np.linalg.norm(vec1)*(np.linalg.norm(vec2)))

    return similarity >= 0.4


def benchmarks_wordbag(data_path: str):
    with open(data_path, encoding='utf-8') as f:
        raw_file = json.load(f)

    print(f'*****{data_path}***wordbag*****\n')

    for _type, data in raw_file['data'].items():
        total_number = 0
        similar_number = 0
        similar_ids = []
        for item in data:
            is_similar = wordbag_similar(item['reqs'][0], item['reqs'][1])
            if is_similar:
                similar_number += 1
                similar_ids.append(item['id'])
            total_number += 1

        print(
            f'Type: {_type};\n'
            f'Total: {total_number};\n'
            f'Similar: {similar_number};\n'
            f'Similar Ids: {similar_ids}.\n'
        )


def benchmarks_simreqs(data_path: str):
    with open(data_path, encoding='utf-8') as f:
        raw_file = json.load(f)

    print(f'*****{data_path}***simreqs*****\n')

    for _type, data in raw_file['data'].items():
        total_number = 0
        similar_number = 0
        similar_ids = []
        for item in data:
            is_similar = is_reqs_similar(item['reqs'][0], item['reqs'][1], _type)
            if is_similar:
                similar_number += 1
                similar_ids.append(item['id'])
            total_number += 1

        print(
            f'Type: {_type};\n'
            f'Total: {total_number};\n'
            f'Similar: {similar_number};\n'
            f'Similar Ids: {similar_ids}.\n'
        )


def benchmarks(data_dir: str):
    similar_reqs_raw = op.join(data_dir, 'similar_reqs_raw.json')
    similar_reqs_structured = op.join(data_dir, 'similar_reqs_structured.json')
    nsimilar_reqs_raw = op.join(data_dir, 'nsimilar_reqs_raw.json')
    nsimilar_reqs_structured = op.join(data_dir, 'nsimilar_reqs_structured.json')

    benchmarks_simreqs(similar_reqs_structured)
    benchmarks_simreqs(nsimilar_reqs_structured)
    benchmarks_wordbag(similar_reqs_raw)
    benchmarks_wordbag(nsimilar_reqs_raw)
