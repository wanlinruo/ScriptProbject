# -*- coding: UTF-8 -*-
import random

import requests as requests

from util.log_util import logger

# 全局请求配置
request = requests.Session()
# ip代理池
ip_list = [
    '118.254.159.100:4220',
    '112.132.49.95:4226',
    '182.136.101.75:4256',
    '49.89.151.87:4245',
    '121.226.212.141:4245',
    '27.153.201.80:4258',
    '113.243.33.78:4243',
    '117.95.114.161:4236',
    '115.212.39.112:4234',
    '121.234.198.16:4236',
    '221.199.195.137:4245',
    '117.89.160.29:4254',
    '221.199.195.138:4245',
    '222.78.209.119:4278',
    '110.18.2.123:4234',
    '140.255.42.219:4258',
    '223.215.104.123:4285',
    '113.226.100.96:4286',
    '140.255.41.124:4258',
    '120.38.216.118:4278',
    '110.90.137.91:4213',
    '106.32.13.12:4245',
    '27.9.50.174:4220',
    '180.109.147.147:4254',
    '36.33.22.197:4226',
    '120.34.216.149:4245',
    '125.87.80.214:4278',
    '36.32.44.110:4226',
    '125.87.86.218:4278',
    '36.35.5.136:4226',
    '125.44.70.31:4245',
    '114.233.70.223:4216',
    '60.166.182.105:4263',
    '117.94.245.114:4257',
    '115.211.43.105:4274',
    '49.85.31.120:4257',
    '114.233.50.170:4257',
    '222.141.186.166:4210',
    '106.111.14.3:4257',
]
user_agent_list = [
    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2224.3 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.2; Win64; x64; rv:21.0.0) Gecko/20121011 Firefox/21.0.0",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:64.0) Gecko/20100101 Firefox/64.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10; rv:33.0) Gecko/20100101 Firefox/33.0",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
    "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
]
# 设置代理
# choice = random.choice(ip_list)choice
# logger.info('choice...' + choice)
# request.proxies = {'https': 'https://' + choice, 'http': 'http://' + choice}
# 设置重试次数
# request.mount('https://', HTTPAdapter(max_retries=3))

# 公共的请求头
common_head = {
    'Host': 'xihuwenti.juyancn.cn',
    'Cookie': 'CNZZDATA1274723626=1000439594-1636897400-%7C1636897400; '
              'WECHAT_OPENID=oAKYc0wChKSJXk-Qt_ZLEsxWraBQ; '
              'OAUTHACCESS=%257B%2522access_token%2522%253A%252251_4FPf5ME7v9ZIndi5nvdtmoRRO_GIl32J8MJstoCBZsoRh1PnSdwsr4C4c-O4UP-_a63cXpnJZ7YduHl84kp2lg%2522%252C%2522expires_in%2522%253A7200%252C%2522refresh_token%2522%253A%252251_s_OljbLSVEN-5mEStqQtz-tRPMC5q-Mmlioo3yo3jcUaSJbwPsFBKbhC7uklZn4ignAESKbkgpKqwHdETEjMFA%2522%252C%2522openid%2522%253A%2522oAKYc0wChKSJXk-Qt_ZLEsxWraBQ%2522%252C%2522scope%2522%253A%2522snsapi_userinfo%2522%252C%2522mid%2522%253A0%257D; '
              'UM_distinctid=17d1eec7ca82ee-0eda95c9a32666-513d0b67-13c680-17d1eec7ca9e69; '
              'PHPSESSID=187d0ngs75djccj4mp1ljnsmf7',
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
