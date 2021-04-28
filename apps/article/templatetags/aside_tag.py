#!/usr/bin/python  
# -*- coding:utf-8 -*-
from datetime import datetime
from datetime import timedelta
from apps.article.models import Article
from django import template

from apps.forum.models import Forum
from apps.user.models import UserMessage

register = template.Library()
@register.inclusion_tag('pc/base_aside.html')
def get_aside():
    popular = Article.objects.filter(is_show=True).order_by('-click_nums')[:5]
    return {'popular':popular}


@register.simple_tag
def get_categories():
    cur_date=datetime.now().date()
    last_month=cur_date-timedelta(days=30)
    popular=Article.objects.filter(create_time__gte=last_month,is_show=True).order_by('-click_nums')[:5]

    return popular
