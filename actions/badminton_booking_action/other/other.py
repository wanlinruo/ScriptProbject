# -*- coding: UTF-8 -*-
from util.log_util import logger
from util.http_util import common_head, request


# 获取支付信息
def get_pay_info(_param):
    logger.info('获取支付信息中...')
    url = "https://xihuwenti.juyancn.cn/wechat/order/bookingorderfee" \
          "?showId=753" \
          "&idNo=" \
          "&certType=10001" \
          "&activityId=0" \
          "&couponId=0" \
          "&cardNo=" \
          "&param=" + _param + "&type=json"
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    }
    headers.update(**common_head)
    request.post(url=url, headers=headers, data="", timeout=2)
