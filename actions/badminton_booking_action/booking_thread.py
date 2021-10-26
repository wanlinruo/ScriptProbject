# -*- coding: UTF-8 -*-
import datetime
import json
import threading
import time
from typing import Tuple, Dict, List

from bs4 import BeautifulSoup

from util.http_util import request, common_head
from util.log_util import logger
from util.time_util import get_day_zero_time


class BookingThread(threading.Thread):

    def __init__(self, target_date_str, booking_place_start_time, place_id):
        threading.Thread.__init__(self)
        self.target_date_str = target_date_str
        self.booking_place_start_time = booking_place_start_time
        self.place_id = place_id

    def run(self):
        print(self.getName())
        ready = self.go_to_ready()
        self.go_to_booking(ready)

    def log_info_tag(self, tips):
        logger.info(f'[{self.getName()}] {tips}')

    def go_to_ready(self):
        self.log_info_tag('go_to_ready...')
        # 标记次数
        running_times = 0
        # 无限循环
        while True:
            running_times += 1
            # 获取预定场地信息
            info = self.get_info()
            # 是否有可选的场地
            if len(info[1]) != 0:
                break
            else:
                self.log_info_tag('暂时无场地可选择*' + str(running_times))

            # 逢100次周期睡眠30秒，避免接口请求频繁被封ip
            if running_times % 100 == 0:
                self.log_info_tag('time.sleep...')
                time.sleep(30)
        return info

    def get_info(self) -> Tuple[Dict[str, str], List[Dict[str, str]]]:
        self.log_info_tag('获取预定场地信息中...')
        # 转换为当天凌晨
        today_zero_time = get_day_zero_time(self.target_date_str)

        url = f'https://xihuwenti.juyancn.cn/wechat/product/details?id={self.place_id}&time=' + str(today_zero_time)
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        }
        try:
            headers.update(**common_head)
            response = request.get(url=url, headers=headers, timeout=3)
            soup = BeautifulSoup(response.text, 'html.parser')
            # 定义搜索结果
            result_list = []
            find_all = soup.findAll('li')
            for li in find_all:
                if str(li).__contains__('class="a-default can-select"'):
                    li_str = 'data-start="%s"' % self.booking_place_start_time
                    if str(li).__contains__(li_str):
                        result = {'hall_id': li['data-hall_id'],
                                  'start': li['data-start'],
                                  'end': li['data-end'],
                                  'money': '%.2f' % (float(li['data-price'])),
                                  'cost_price': '%.2f' % (float(li['data-cost_price'])),
                                  'date': str(
                                      datetime.datetime.strptime(self.target_date_str, "%Y-%m-%d %H:%M:%S").date())
                                  }
                        result_list.append(result)
            self.log_info_tag('get_info-response:' + str(list(reversed(result_list))))
            return {'Referer': url, }, list(reversed(result_list))
        except Exception as e:
            self.log_info_tag('get_info e:' + str(e))
        return {'Referer': url, }, []

    def go_to_booking(self, info):
        current_times = 0
        success_times = 0
        limit_times = 2
        # 当还没成功抢票时候，则一直循环，但周期到达50时候，希望已不大
        while success_times < limit_times and current_times <= 50:
            for can_select in info[1]:
                # 判定是否到达限制
                if success_times < limit_times:
                    order = self.go_to_save_order(info[0], can_select)
                    # 成功则进行
                    if order[0]:
                        pay_result = self.go_to_pay(order[1])
                        # 成功则进行
                        if pay_result:
                            success_times += 1
                            self.log_info_tag('抢票*' + str(success_times) + '成功...')
            # 周期++
            current_times += 1
            self.log_info_tag('周期循环*' + str(current_times) + '...')

    def go_to_save_order(self, _referer, _info) -> Tuple[bool, str]:
        self.log_info_tag('go_to_save_order...')
        url = 'https://xihuwenti.juyancn.cn/wechat/product/save'
        headers = {
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'X-Requested-With': 'XMLHttpRequest',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Referer': _referer['Referer'],
        }
        headers.update(**common_head)

        data = {
            'show_id': self.place_id,
            'date': _info['date'],
            'data[]': _info['hall_id'] + ',' + _info['start'] + ',' + _info['end'],
            'money': _info['money'],
            'total_fee': _info['cost_price'],
        }
        try:
            response = request.post(url=url, headers=headers, data=data, timeout=3)
            loads = json.loads(response.text)
            # 打印结果
            self.log_info_tag('go_to_save_order-response:' + str(loads))
            if loads['code'] == 0:
                # 成功则直接回传参数
                return True, loads['msg']
        except Exception as e:
            self.log_info_tag('go_to_save_order e:' + str(e))
        # 失败的统一回传
        return False, ''

    def go_to_pay(self, _param):
        self.log_info_tag('获取支付记录中...')
        url = 'https://xihuwenti.juyancn.cn/wechat/order/add'
        headers = {
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'X-Requested-With': 'XMLHttpRequest',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Origin': 'https://xihuwenti.juyancn.cn',
            'Referer': f'https://xihuwenti.juyancn.cn/wechat/order/index?show_id={self.place_id}&param=' + _param,
        }
        headers.update(**common_head)

        data = {
            'show_id': self.place_id,
            'username': '万林若',
            'mobile': '18826243441',
            'smscode': '',
            'id_card': '441424199407170535',
            'certType': '10001',
            'param': _param,
            'activityid': '0',
            'couponId': '0',
        }
        try:
            response = request.post(url=url, headers=headers, data=data, timeout=3)
            self.log_info_tag('go_to_pay response:' + str(response))
            loads = json.loads(response.text)
            self.log_info_tag('go_to_pay response-json:' + str(loads))
            # 判断是否成功
            if loads['code'] == 0:
                # 成功则机器人通知
                # push_job()
                return True
        except Exception as e:
            self.log_info_tag('go_to_pay e:' + str(e))
        # 失败统一回传
        return False
