# -*- coding: UTF-8 -*-

import requests as requests
from requests.adapters import HTTPAdapter

# 设置重试次数
request = requests.Session()
request.mount('https://', HTTPAdapter(max_retries=3))

# 公共的请求头
common_head = {
    'Host': 'xihuwenti.juyancn.cn',
    'Cookie': 'CNZZDATA1274723626=1490805407-1630140490-%7C1630140490; '
              'WECHAT_OPENID=oAKYc03bKKdxKrjxRlid29eWSlLY; '
              'UM_distinctid=17b8c5ce6784b-09d7980877b4a1-6e375e39-13c680-17b8c5ce67911f2; '
              'PHPSESSID=5o7vskjb8hpk8mr4ogeg9t3pj7',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_16) '
                  'AppleWebKit/605.1.15 (KHTML, like Gecko) '
                  'MicroMessenger/6.8.0(0x16080000) '
                  'MacWechat/3.1.5(0x13010513) '
                  'NetType/WIFI WindowsWechat',
    'Accept-Language': 'zh-cn',
    'Origin': 'https://xihuwenti.juyancn.cn',
}
