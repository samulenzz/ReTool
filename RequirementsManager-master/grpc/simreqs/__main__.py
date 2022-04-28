import fire

from simreqs.process_corpus.process_corpus import (
    process_wikizh_corpus, process_newszh_corpus,
    process_baikeqazh_corpus
)
from simreqs.train.train import train_model
from simreqs.similarity import sentence_similarity
from simreqs.demo import run_demo
from simreqs.benchmarks import benchmarks


if __name__ == '__main__':
    fire.Fire({
        'process_corpus': {
            'wikizh': process_wikizh_corpus,
            'newszh': process_newszh_corpus,
            'baikeqazh': process_baikeqazh_corpus
        },
        'train': train_model,
        'sentence_similarity': sentence_similarity,
        'run_demo': run_demo,
        'benchmarks': benchmarks,
    })
