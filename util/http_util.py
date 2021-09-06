# -*- coding: UTF-8 -*-

import requests as requests
from requests.adapters import HTTPAdapter

# 全局请求配置
request = requests.Session()
# 设置代理
# request.proxies = {}
# 设置重试次数
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

'''
https://www.zenrows.com/blog/stealth-web-scraping-in-python-avoid-blocking-like-a-ninja
优化方向：
1、轮换用户代理头
import requests 
import random 
 
user_agents = [ 
	'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36', 
	'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36', 
	'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36', 
	'Mozilla/5.0 (iPhone; CPU iPhone OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148', 
	'Mozilla/5.0 (Linux; Android 11; SM-G960U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.72 Mobile Safari/537.36' 
] 
user_agent = random.choice(user_agents) 
headers = {'User-Agent': user_agent} 
response = requests.get('https://httpbin.org/headers', headers=headers) 
print(response.json()['headers']['User-Agent']) 
# Mozilla/5.0 (iPhone; CPU iPhone OS 12_2 like Mac OS X) ...

2、
'''
