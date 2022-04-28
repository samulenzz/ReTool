import os
import os.path as op
import json

import jieba

from simreqs.logger import logger
from simreqs.utils import get_all_files


def _is_drop_word(word: str) -> bool:
    """是否舍弃单词"""
    for char in word:
        if char >= '\u4e00' and char <= '\u9fa5':
            continue
        if char in ['，', '。']:
            continue
        return True

    return False


def _pre_process_text(text: str) -> str:
    """对字符串进行预处理，包括：分词、除去非汉字..."""
    cut_text = jieba.cut(text)
    filter_cut_text = [
        word for word in cut_text
        if not _is_drop_word(word)
    ]
    return ' '.join(filter_cut_text)


def process_wikizh_corpus(corpus_dir: str, odir: str):
    """
    https://github.com/brightmart/nlp_chinese_corpus
    wiki_zh corpus
    """
    corpus_files = get_all_files(corpus_dir)
    os.makedirs(odir, exist_ok=True)

    counter = 0
    # 遍历，处理语料库
    for corpus_file in corpus_files:
        with open(corpus_file, encoding='utf-8') as fcorpus:
            tmp_text = ''
            for line in fcorpus:
                text = json.loads(line)['text']
                # 预处理，按'\n'划分一下段落，以免一句话过长
                for graph in text.split('\n'):
                    tmp_pre_processed_text = _pre_process_text(graph)
                    if tmp_pre_processed_text:
                        tmp_text += tmp_pre_processed_text + '\n'

            opath = op.join(odir, f'{counter}.txt')
            with open(opath, 'w', encoding='utf-8') as fout:
                fout.write(tmp_text)

        counter += 1
        if counter % 10 == 0:
            logger.info(f'Processed {counter} wikizh files...')


def process_newszh_corpus(corpus_file: str, odir: str):
    """
    https://github.com/brightmart/nlp_chinese_corpus
    news_zh corpus
    """
    os.makedirs(odir, exist_ok=True)

    counter = 0
    with open(corpus_file, encoding='utf-8') as fcorpus:
        tmp_text = ''
        # 每一行都是一个json
        for line in fcorpus:
            text = json.loads(line)['content']
            # 以句号简单划分，遍历
            for sentence in text.split('。'):
                tmp_pre_processed_text = _pre_process_text(sentence)
                if tmp_pre_processed_text:
                    tmp_text += tmp_pre_processed_text + '\n'

            counter += 1
            if counter % 1000 == 0:
                opath = op.join(odir, f'{counter // 1000}.txt')
                with open(opath, 'w', encoding='utf-8') as fout:
                    fout.write(tmp_text)
                logger.info(f'Processed {counter} news articles...')
                tmp_text = ''


def process_baikeqazh_corpus(corpus_file: str, odir: str):
    """
    https://github.com/brightmart/nlp_chinese_corpus
    baikeqa_zh corpus
    """
    os.makedirs(odir, exist_ok=True)

    counter = 0
    with open(corpus_file, encoding='utf-8') as fcorpus:
        tmp_text = ''
        # 每一行都是一个json
        for line in fcorpus:
            text = json.loads(line)['answer']
            # 以句号简单划分，遍历
            for sentence in text.split('。'):
                tmp_pre_processed_text = _pre_process_text(sentence)
                if tmp_pre_processed_text:
                    tmp_text += tmp_pre_processed_text + '\n'

            counter += 1
            if counter % 5000 == 0:
                opath = op.join(odir, f'{counter // 5000}.txt')
                with open(opath, 'w', encoding='utf8') as fout:
                    fout.write(tmp_text)
                logger.info(f'Processed {counter} answers...')
                tmp_text = ''
