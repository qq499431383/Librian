import yaml
import os
import logging


from . import psd拆包
from . import 虛擬機環境

角色表 = {}


def 取角色(名字):
    if 名字 in 角色表:
        return 角色表[名字]
    else:
        return 角色(名字)


def 導入有立繪的角色():
    try:
        with open(f'{虛擬機環境.psd路徑}/映射.yaml', encoding='utf8') as f:
            映射 = yaml.load(f)
            if 映射:
                for i in 映射:
                    角色(i, 映射[i])
                    if not os.path.isdir('%s/%s' % (虛擬機環境.圖片路徑, i)):
                        psd拆包.拆包(f'{虛擬機環境.psd路徑}/{i}.psd', 虛擬機環境.圖片路徑)
            for i in os.listdir(虛擬機環境.psd路徑):
                if i.endswith('.png'):
                    前名 = os.path.basename(os.path.splitext(i)[0])
                    if not os.path.isdir('%s/%s' % (虛擬機環境.圖片路徑, 前名)):
                        全名 = os.path.join(虛擬機環境.psd路徑, i)
                        psd拆包.png假裝拆包(全名, 虛擬機環境.圖片路徑)
                    角色(前名, {
                        '衣': {'_默認': ['_']},
                        '顏': {'_默認': []},
                    })
    except Exception as e:
        logging.warning(e.__repr__())
        logging.warning('角色立繪沒有導入。')


class 角色:
    def __init__(self, 名字, 立繪表=None):
        self.名字 = 名字
        self.顯示名字 = None

        self.有立繪 = bool(立繪表)
        if self.有立繪:
            with open('%s/%s/位置.yaml' % (虛擬機環境.圖片路徑, self.名字), encoding='utf8') as f:
                self.圖層座標 = yaml.load(f)

            self.衣圖層 = 立繪表['衣']
            self.顏圖層 = 立繪表['顏']
            self.固有縮放 = 立繪表.get('縮放', 1)
            self.現顏 = '_默認'
            self.現衣 = '_默認'
            self.現特效 = None
        else:
            logging.warning(f'新建了沒有立繪的角色「{名字}」')

        assert self.名字 not in 角色表
        角色表[self.名字] = self

    @property
    def 現衣圖層(self):
        try:
            return self.衣圖層[self.現衣 or '_默認']
        except:
            logging.warning(f'衣「{self.現衣}」沒有配置。')
            return []

    @property
    def 現顏圖層(self):
        try:
            return self.顏圖層[self.現顏 or '_默認']
        except:
            logging.warning(f'顏「{self.現顏}」沒有配置。')
            return []

    def 定座標(self, 圖層):
        return self.圖層座標[圖層]['x'], self.圖層座標[圖層]['y']

    def __repr__(self):
        return f'角色{"|"+self.顯示名字 if self.顯示名字 else ""}({self.名字}->[衣:{self.衣圖層}],[顏:{self.顏圖層}])'


導入有立繪的角色()
