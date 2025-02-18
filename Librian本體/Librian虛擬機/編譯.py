import re
import logging

正則組 = {
    '^> *(?P<原文>(?P<函數>\S*)(?P<參數表>(.*)))$': {
        '類型': '函數調用',
        '子樹': {
            '參數表': {
                '(?P<a>(((?<=").*?(?="))|(((?<= )|(?<=^))([^" ]+?)(?=( |$)))))': None
            }
        }
    },
    '^```(?P<代碼類型>.*?)\n(?P<代碼內容>(.|\\n)*?)\\n```$': {
        '類型': '插入代碼'
    },
    '^@ *(?P<人物名>.+?) *(?P<操作符>[\\+\\|]) *(?P<目標>.+?)$': {
        '類型': '人物操作'
    },
    '^={3,} *(?P<插入圖>.*) *$': {
        '類型': '插入圖',
    },
    '^(?P<名>.+?)(\|(?P<代>.+?))? +(\[(?P<特效>.+?)\])? *(\((?P<顏>.+?)\))? *(「|“)(?P<語>(.|\\n)*?)(”|」) *$': {
        '類型': '人物對話',
    },
    '^(?P<名>.+?)(\|(?P<代>.+?))?  *(\[(?P<特效>.+?)\])? *(\((?P<顏>.+?)\)) *$': {
        '類型': '人物表情',
    },
    '^(?P<鏡頭符號>[\\+\\-]) *(?P<內容>.*)$': {
        '類型': '鏡頭',
    },
    '^#(?P<註釋>.*)$': {
        '類型': '註釋',
    },
    '^\\*(?P<躍點>.*)$': {
        '類型': '躍點'
    }
}
續行組 = {
    '^(.+?)(\|(.+?))? (\((.+?)\))?「([^」]*)$',
    r'^```(.|\n)*(?<!\n```)$'
}
錯誤組 = {
    '^.*?「[^」]*「.*$':
        '引號不匹配'
}


def 遞歸re(s, start=正則組):
    d = []
    for i in start:
        單位 = re.finditer(i, s)
        for j in 單位:
            gd = j.groupdict()
            d.append(gd)
            if isinstance(start[i], dict):
                gd['類型'] = start[i]['類型']
            if start[i] is not None and '子樹' in start[i]:
                for k in start[i]['子樹']:
                    gd[k] = 遞歸re(gd[k], start[i]['子樹'][k])
    return d


class j棧(list):
    def __init__(self):
        self.append([])

    @property
    def 尾(self):
        return self[-1]

    @property
    def 尾句(self):
        return self[-1][-1]


def 編譯(f):
    return 生編譯(f.readlines())


def 生編譯(t):
    棧 = j棧()
    多行緩衝 = ''
    for 當前行 in iter(t):
        if not re.search('\\S', 當前行):
            if 棧.尾:
                棧.尾句['之後的空白'] = 棧.尾句.get('之後的空白', 0) + 1
            continue
            
        當前行 = 當前行.rstrip('\r').rstrip('\n')
        if 多行緩衝:
            當前行 = 多行緩衝 + '\n' + 當前行
            多行緩衝 = ''
        if any([re.match(i, 當前行) for i in 續行組]):
            多行緩衝 = 當前行
            logging.debug(多行緩衝)
            continue
                
        自 = {}
        自['縮進數'] = len(當前行) - len(當前行.lstrip(' '))
        if 自['縮進數'] > 0 and 自['縮進數'] > 棧.尾句['縮進數']:
            棧.尾句['子'] = []
            棧.append(棧.尾句['子'])

        if 棧.尾:
            while 自['縮進數'] < 棧.尾句['縮進數']:
                棧.pop()
            if 棧.尾句['縮進數'] != 自['縮進數']:
                raise Exception('層次錯誤')

        當前行 = 當前行.lstrip(' ').rstrip(' ')
        for 表達式, 信息 in 錯誤組.items():
            if re.match(表達式, 當前行):
                raise Exception(f'『{當前行}』有語法錯誤——{信息}。')
        d = 遞歸re(當前行)
        if not d:
            d.append({'類型': '旁白', '旁白': 當前行})
        if len(d) > 1:
            raise Exception(f'『{當前行}』匹配過多，有可能是【{"，".join([i["類型"] for i in d])}】')
        自.update(d[0])

        棧.尾.append(自)
    return 棧[0]


def 印(q):
    for i in q:
        if '子' in i:
            t = i['子']
            del i['子']
            print(' ' * i['縮進數'], end='')
            del i['縮進數']
            print(i)
            印(t)
        else:
            print(' ' * i['縮進數'], end='')
            del i['縮進數']
            print(i)


if __name__ == '__main__':
    with open('1.liber', encoding='utf8') as f:
        印(編譯(f))
        # print(編譯(f))
