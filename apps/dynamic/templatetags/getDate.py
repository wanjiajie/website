#!/usr/bin/python  
# -*- coding:utf-8 -*-  
# @Time    : 2021/4/27 16:41 下午
# @Author  : wanjiajie
# @Email   : 1242493979@qq.com
# @File    : getDate.py
# @Software: Vscode
import pytz
from django import template
from datetime import datetime
register = template.Library()

@register.filter
def getTimer(data):
    if isinstance(data, datetime):
        # 获取最新时间
        now = datetime.now()
        #now = now.replace(tzinfo=pytz.timezone('UTC'))
        # 确定settings里面的设置
        #print('最新时间{}'.format(now))  # 大陆时间
        #print('数据库的时间{}'.format(data))
        #减去相差得到天数并且转化时间戳
        timestamp = (now - data).total_seconds()

        if timestamp < 60:
            return '刚刚'
        elif timestamp >= 60 and timestamp < 60 * 60:
            minu = int(timestamp // 60)
            return '{}分钟前'.format(minu)
        elif timestamp >= 60 * 60 and timestamp < 60 * 60 * 24:
            hour = int(timestamp // (60 * 60))
            return '{}小时前'.format(hour)
        elif timestamp >= 60 * 60 * 24 and timestamp < 60 * 60 * 24 * 30:
            day = int(timestamp // (60 * 60 * 24))
            return '{}天前'.format(day)
        elif timestamp >= 60 * 60 * 24 * 30 and timestamp < 60 * 60 * 24 * 365:
            mon = int(timestamp // (60 * 60 * 24 * 30))
            return '{}月前'.format(mon)
        elif timestamp >= 60 * 60 * 24 * 365 and timestamp < 60 * 60 * 24 * 365 * 2:
            year = int(timestamp // (60 * 60 * 24 * 365))
            return '{}年前'.format(year)
        else:
            #return data.strftime('%Y-%m-%d %H:%M')
            return data
    else:
        return data