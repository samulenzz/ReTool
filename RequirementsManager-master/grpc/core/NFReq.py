class NFReq(object):
    def __init__(self, text):
        self.vtype = ''
        self.rtype = ''
        self.sign = ''
        self.value = 0
        self.unit = ''

        # 识别比较符
        sign_words = {'>': ['大于', '超过', '高于', '多于'],
                      '<': ['小于', '不足', '低于', '少于'],
                      '=': ['等于']}
        begin, end = 0, 0
        for word in sign_words['>']:
            begin = text.rfind(word)
            if begin > 0:
                end = begin + len(word)
                if text[begin - 1] == '不':
                    self.sign = '5'
                    begin -= 1
                else:
                    self.sign = '2'
                break
        if self.sign == '':
            for word in sign_words['<']:
                begin = text.rfind(word)
                if begin > 0:
                    end = begin + len(word)
                    if text[begin - 1] == '不':
                        self.sign = '4'
                        begin -= 1
                    else:
                        self.sign = '1'
                    break
        if self.sign == '':
            for word in sign_words['=']:
                begin = text.rfind(word)
                if begin > 0:
                    end = begin + len(word)
                    if text[begin - 1] == '不':
                        self.sign = '6'
                        begin -= 1
                    else:
                        self.sign = '3'
                    break
        if self.sign == '':
            return

        # 从end开始，到标点符号结束，分开 性能值 和 单位
        punc_index = text.find('，')
        if punc_index < 0:
            punc_index = text.find('。')
        subtext = text[end: punc_index]
        # 寻找数字的结尾
        num_word = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '.',
                    '一', '二', '三', '四', '五', '六', '七', '八', '九', '零',
                    '十', '百', '千', '万', '亿', '兆']
        index = 0
        while True:
            if subtext[index] not in num_word:
                break
            index += 1
        if index == 0:
            print(text)
            return
        self.value = subtext[:index]
        self.unit = subtext[index:]

        rtype_words = ['平均', '最大', '最小', ]
        subtext = text[:begin]
        index = -1
        for word in rtype_words:
            index = subtext.find(word)
            if index > 0:
                self.rtype = word
                break
        self.vtype = subtext[:index] if index > 0 else subtext

        d_rtype = {'': '0', '最大': '1', '最小': '2', '平均': '3', }
        self.rtype = d_rtype[self.rtype]


    @classmethod
    def parse_req(cls, text):
        text_list = text.split('，')
        for t in text_list:
            r = NFReq(t)
            if r.sign != '':
                return r
