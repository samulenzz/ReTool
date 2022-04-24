import jieba


class judgeSimilarity:
    def __init__(self, stopwords):
        self.stop_words_set = set(stopwords)

    def is_similar(self, s1: str, s2: str) -> bool:
        return True


if __name__ == '__main__':
    stopwords_list = []
    # stopwords_file_path = ''
    # with open(stopwords_file_path, 'r') as f:
    #     for word in f:
    #         stopwords_list.append(word.strip())
    judge = judgeSimilarity(stopwords_list)
    s1 = '广告太多了'
    s2 = '希望广告少一点'
    print(judge.is_similar(s1, s2))
