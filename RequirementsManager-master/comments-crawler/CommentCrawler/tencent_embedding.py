from gensim.models import KeyedVectors
import numpy as np

import warnings

MAX_WORD_COUNT = 1000000

# https://ai.tencent.com/ailab/nlp/zh/embedding.html
# 800多万中文词汇，其中每个词对应一个200维

if __name__ == '__main__':
    warnings.filterwarnings('ignore')

    file = '../tecent_ailab_word2vec/Tencent_AILab_ChineseEmbedding.txt'
    wv_from_text = KeyedVectors.load_word2vec_format(
        file, binary=False, limit=MAX_WORD_COUNT)
    wv_from_text.init_sims(replace=True)
    print(wv_from_text)
    word_list = ['为什么', '新的', '会', '添加', '不', '了', '朋友']
    res = np.zeros(200)
    for word in word_list:
        try:
            res += wv_from_text.get_vector(word)
        except:
            pass
    print(res.tolist())
    # word = '膝关节置换手术'
    # if word in wv_from_text.wv.vocab.keys():
    #     vec = wv_from_text[word]
    #     print(wv_from_text.most_similar(positive=[vec], topn=20))
    # else:
    #     print("没找到")
