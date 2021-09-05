# -*- coding: UTF-8 -*-
import time
import datetime


def get_day_zero_time(target_date_str):
    """根据日期获取当天凌晨时间"""
    if not target_date_str:
        return 0
    # 把字符串转成datetime
    date = datetime.datetime.strptime(target_date_str, "%Y-%m-%d %H:%M:%S")

    date_zero = datetime.datetime.now().replace(year=date.year, month=date.month,
                                                day=date.day, hour=0, minute=0, second=0)
    date_zero_time = int(time.mktime(date_zero.timetuple()))
    return date_zero_time
