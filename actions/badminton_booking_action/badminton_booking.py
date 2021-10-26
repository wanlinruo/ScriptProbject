# -*- coding: UTF-8 -*-

import datetime

from chinese_calendar import is_workday

from actions.badminton_booking_action.booking_thread import BookingThread
from util.log_util import logger


def set_time_desc() -> tuple[str, dict[str, list[str]]]:
    logger.info('set_time_desc...')
    # 获取五天后的凌晨时间戳（秒）
    target_date = datetime.datetime.now() + datetime.timedelta(days=4)
    logger.info('预定票日期：' + str(target_date.date()))

    # 抢票预定地方的场次开始时间
    # 区分工作日和周末
    current_date = datetime.datetime.now().date()
    if is_workday(current_date):
        start_time_list = ['20:00']
    else:
        start_time_list = ['18:00', '20:00']

    logger.info('预定票场次时间（开始时间为准）：' + str(start_time_list))

    # 预定的场地id
    # 西湖文体3楼-->753
    # 西湖文体1楼-->752
    place_id_list = ['753', '752']
    place_time_map = {}

    for place_id_item in place_id_list:
        place_time_map[f'{place_id_item}'] = start_time_list

    # 把datetime转成字符串
    return target_date.strftime("%Y-%m-%d %H:%M:%S"), place_time_map


def job():
    logger.info('开始抢票...')
    desc = set_time_desc()

    for place_time_item in desc[1]:
        time_list = desc[1][place_time_item]
        for time_item in time_list:
            # 准备数据
            print(f'desc[0]:{desc[0]}')
            print(f'time_item:{time_item}')
            print(f'place_time_item:{place_time_item}')
            thread = BookingThread(desc[0], time_item, place_time_item)
            thread.start()
            # thread.join()

    logger.info('结束抢票...')


if __name__ == '__main__':
    # scheduler = BlockingScheduler()
    # scheduler.add_job(job, 'cron', hour=8, minute=59, second=55)
    # scheduler.add_job(job, 'cron', hour='9', minute=9, second=55)
    # scheduler.start()
    job()
