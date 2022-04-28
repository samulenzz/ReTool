import os
import os.path as op

from gensim.models import Word2Vec

from simreqs.train.sentences import MySentences


def train_model(corpus_dir: str,
                odir: str,
                size: int = 128,
                window: int = 5,
                min_count: int = 5,
                workers: int = 5):

    sentences = MySentences(corpus_dir)
    model = Word2Vec(
        sentences, size=size, window=window,
        min_count=min_count, workers=workers
    )

    os.makedirs(odir, exist_ok=True)
    opath = op.join(odir, 'word2vec.model')
    model.save(opath)
