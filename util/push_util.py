# -*- coding: UTF-8 -*-

import json
from util.http_util import request


def push_job():
    url = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=e3446ff1-238a-4bca-a32d-3862857b7c4e"

    start_data = {
        "msgtype": "markdown",
        "markdown": {
            "content": "西湖文体羽毛球场地预定成功，请尽快到手机上进行确认！"
        }
    }

    params = json.dumps(start_data, ensure_ascii=True)
    request.post(url, params)
