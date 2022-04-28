# 需求整体标识  需求条目类型   条目内容   性能指标  比较符1  持续时间数值  比较符2  概率
#     id           type     description  vtype    sign1     duration    sign2    pr

class RelReq(object):
    def __init__(self, text: str):
        self.vtype = ''
        self.sign1 = ''
        self.duration = ''
        self.sign2 = ''
        self.pr = ''

        sign_words = {'>': ['大于', '超过', '高于', '多于'],
                      '<': ['小于', '不足', '低于', '少于'],
                      '=': ['等于']}
        not_word = {'<': '>=', '>': '<=', '=': '!='}

        # 识别比较符
        begin_list, end_list, sign_list = [], [], []
        for sign, word_list in sign_words.items():
            for word in word_list:
                begin = text.find(word)
                if begin > 0:
                    end = begin + len(word)
                    if text[begin - 1] == '不':
                        begin -= 1
                        sign_list.append(not_word[sign])
                    else:
                        sign_list.append(sign)
                    begin_list.append(begin)
                    end_list.append(end)
                    begin = text.find(word, end)
                    if begin > 0:
                        end = begin + len(word)
                        if text[begin - 1] == '不':
                            begin -= 1
                            sign_list.append(not_word[sign])
                        else:
                            sign_list.append(sign)
                        begin_list.append(begin)
                        end_list.append(end)
        # assert len(begin_list) == len(end_list) == len(sign_list) == 2
        if not (len(begin_list) == len(end_list) == len(sign_list) == 2):
            return
        if begin_list[1] < begin_list[0]:
            begin_list.reverse()
            end_list.reverse()
            sign_list.reverse()
        self.sign1 = sign_list[0]
        self.sign2 = sign_list[1]

        # 性能指标
        self.vtype = text[:begin_list[0]]

        # 概率
        pr = text[end_list[1]:]
        self.pr = pr[:-1] if pr[-1] == '。' else pr

        # 持续时间数值
        text = text[end_list[0]: begin_list[1]]
        num_word = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '.',
                    '一', '二', '三', '四', '五', '六', '七', '八', '九', '零',
                    '十', '百', '千', '万', '亿', '兆', '半']
        begin, end = -1, -1
        for num in num_word:
            begin = text.find(num)
            if begin >= 0:
                break
        time_word = ['秒', '分钟', '小时', '天', '月', '年']
        for time in time_word:
            index = text.rfind(time)
            if index >= 0:
                if index + len(time) > end:
                    end = index + len(time)
        # assert begin >= 0 and end >= 0
        if begin >= 0 and end >= 0:
            self.duration = text[begin: end]

        # 替换比较符
        sign_dict = {'<': '1', '>': '2', '=': '3', '>=': '4', '<=': '5', '!=': '6'}
        self.sign1 = sign_dict[self.sign1]
        self.sign2 = sign_dict[self.sign2]


    @classmethod
    def parse_req(cls, text):
        r = RelReq(text)
        if r.vtype == r.sign1 == r.duration == r.sign2 == r.pr == '':
            return None
        return r
