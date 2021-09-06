# -*- coding: UTF-8 -*-
import datetime
import json
from typing import Tuple, Dict, List

from bs4 import BeautifulSoup

from util.http_util import request, common_head
from util.log_util import logger
from util.push_util import push_job
from util.time_util import get_day_zero_time
from apscheduler.schedulers.blocking import BlockingScheduler


def set_time_desc() -> Tuple[str, str]:
    logger.info('set_time_desc...')
    # 获取五天后的凌晨时间戳（秒）
    target_date = datetime.datetime.now() + datetime.timedelta(days=4)
    logger.info('预定票日期：' + str(target_date.date()))

    # 抢票预定地方的场次开始时间
    booking_place_start_time = '20:00'
    logger.info('预定票场次时间（开始时间为准）：' + str(booking_place_start_time))

    # 把datetime转成字符串
    return target_date.strftime("%Y-%m-%d %H:%M:%S"), booking_place_start_time


def go_to_ready(target_date_str, booking_place_start_time):
    logger.info('go_to_ready...')
    # 标记次数
    running_times = 0
    # 无限循环
    while True:
        running_times += 1
        # 获取预定场地信息
        info = get_info(target_date_str, booking_place_start_time)
        # 是否有可选的场地
        if len(info[1]) != 0:
            break
        else:
            logger.info('暂时无场地可选择*' + str(running_times))
    return info


def get_info(target_date_str, _booking_place_start_time) -> Tuple[Dict[str, str], List[Dict[str, str]]]:
    logger.info('获取预定场地信息中...')
    # 转换为当天凌晨
    today_zero_time = get_day_zero_time(target_date_str)

    url = 'https://xihuwenti.juyancn.cn/wechat/product/details?id=753&time=' + str(today_zero_time)
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
                li_str = 'data-start="%s"' % _booking_place_start_time
                if str(li).__contains__(li_str):
                    result = {'hall_id': li['data-hall_id'],
                              'start': li['data-start'],
                              'end': li['data-end'],
                              'money': '%.2f' % (float(li['data-price'])),
                              'cost_price': '%.2f' % (float(li['data-cost_price'])),
                              'date': str(datetime.datetime.strptime(target_date_str, "%Y-%m-%d %H:%M:%S").date())
                              }
                    result_list.append(result)
        logger.info('get_info-response:' + str(list(reversed(result_list))))
        return {'Referer': url, }, list(reversed(result_list))
    except Exception as e:
        logger.info('get_info e:' + str(e))
    return {'Referer': url, }, []


def go_to_booking(info):
    current_times = 0
    success_times = 0
    limit_times = 2
    # 当还没成功抢票时候，则一直循环，但周期到达50时候，希望已不大
    while success_times < limit_times and current_times <= 50:
        for can_select in info[1]:
            # 判定是否到达限制
            if success_times < limit_times:
                order = go_to_save_order(info[0], can_select)
                # 成功则进行
                if order[0]:
                    pay_result = go_to_pay(order[1])
                    # 成功则进行
                    if pay_result:
                        success_times += 1
                        logger.info('抢票*' + str(success_times) + '成功...')
        # 周期++
        current_times += 1
        logger.info('周期循环*' + str(current_times) + '...')


def go_to_save_order(_referer, _info) -> Tuple[bool, str]:
    logger.info('go_to_save_order...')
    url = 'https://xihuwenti.juyancn.cn/wechat/product/save'
    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'X-Requested-With': 'XMLHttpRequest',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Referer': _referer['Referer'],
    }
    headers.update(**common_head)

    data = {
        'show_id': '753',
        'date': _info['date'],
        'data[]': _info['hall_id'] + ',' + _info['start'] + ',' + _info['end'],
        'money': _info['money'],
        'total_fee': _info['cost_price'],
    }
    try:
        response = request.post(url=url, headers=headers, data=data, timeout=3)
        loads = json.loads(response.text)
        # 打印结果
        logger.info('go_to_save_order-response:' + str(loads))
        if loads['code'] == 0:
            # 成功则直接回传参数
            return True, loads['msg']
    except Exception as e:
        logger.info('go_to_save_order e:' + str(e))
    # 失败的统一回传
    return False, ''


def go_to_pay(_param):
    logger.info('获取支付记录中...')
    url = 'https://xihuwenti.juyancn.cn/wechat/order/add'
    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'X-Requested-With': 'XMLHttpRequest',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Origin': 'https://xihuwenti.juyancn.cn',
        'Referer': 'https://xihuwenti.juyancn.cn/wechat/order/index?show_id=753&param=' + _param,
    }
    headers.update(**common_head)

    data = {
        'show_id': '753',
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
        response = request.post(url=url, headers=headers, data=data)
        logger.info('go_to_pay response:' + str(response))
        loads = json.loads(response.text)
        logger.info('go_to_pay response-json:' + str(loads))
        # 判断是否成功
        if loads['code'] == 0:
            # 成功则机器人通知
            push_job()
            return True
    except Exception as e:
        logger.info('go_to_pay e:' + str(e))
    # 失败统一回传
    return False


def job():
    logger.info('开始抢票...')
    desc = set_time_desc()
    ready = go_to_ready(desc[0], desc[1])
    go_to_booking(ready)
    logger.info('结束抢票...')


if __name__ == '__main__':
    scheduler = BlockingScheduler()
    scheduler.add_job(job, 'cron', hour='8', minute=59, second=55)
    scheduler.start()
    # job()
