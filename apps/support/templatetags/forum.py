from datetime import datetime

from django.contrib.sessions.models import Session
from django.core.cache import cache

#from apps.forum.views import get_online_count
from apps.support.models import QQ
from apps.forum.models import Forum
from django import template
from django.utils.timezone import now, timedelta
from apps.user.models import User

register = template.Library()
@register.inclusion_tag('pc/aside/forum_side.html')
def get_forum():
    qq = QQ.objects.all()
    forum = Forum.objects.filter(hidden=False,category__name='求职招聘')[:10]
    sessions = Session.objects.filter(expire_date__gte=datetime.now()).count()
    #print(get_online_count())

    user = User.objects.count()
    cur_date = now().date() + timedelta(days=0)
    days = Forum.objects.filter(hidden=False,create_time__gte=cur_date).count()
    count = Forum.objects.filter(hidden=False).count()
    Hottest = Forum.objects.filter(hidden=False).order_by('-click_nums')[:10]
    return {'forum':forum,'qq':qq,'user':user,'sessions':sessions,'days':days,'count':count,'Hottest':Hottest}


@register.filter
def get_count(x):
    return x.filter(hidden=False).count()


@register.filter
def get_counts(x):
    return x.filter(is_show=True).count()