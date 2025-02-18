import os
import logging
import copy

import yaml

from . import 虛擬機環境
from . import 角色


def 人物拆解(包, 參數):
    人 = 角色.取角色(包)
    if not 人.有立繪:
        return None

    位置 = copy.deepcopy(參數['位置'])
    語 = 參數['語']

    動作 = copy.deepcopy(參數['動作'])

    位置[2] *= 人.固有縮放
    if 動作 and 動作[0] == '移動':
        動作[1][2] *= 人.固有縮放
        動作[2][2] *= 人.固有縮放

    回信 = {'圖層': [], '位置': 位置, '動作': 動作, '特效': 人.現特效, '名字': 包}
    衣配件 = 人.現衣圖層[::-1]
    顏 = 人.現顏圖層
    if isinstance(顏, dict):
        if 語:
            顏 = 顏['_語']
        else:
            顏 = 顏['_默認']
    顏配件 = 顏[::-1]
    for 物件 in 衣配件 + 顏配件:
        x, y = 人.定座標(物件)
        回信['圖層'].append(
            {'文件': '%s/%s/%s.png' % (虛擬機環境.圖片相對網頁路徑, 包, 物件),
             '子位置': (x, y)}
        )
    return 回信
