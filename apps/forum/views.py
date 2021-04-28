import re
from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.contrib.sessions.models import Session
from django.core.cache import cache
from django.core.paginator import PageNotAnInteger
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.http import JsonResponse
from django.shortcuts import render, reverse, redirect, get_object_or_404

# Create your views here.
from django_filters.rest_framework import DjangoFilterBackend
from pure_pagination import Paginator
from rest_framework import mixins, viewsets
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from apps.article.views import StandardResultsSetPagination
from apps.forum.filter import ForumFilter
from apps.forum.forms import Forum_form, ParentComment
from apps.forum.models import Forum_template, Forum, Comment, Parent_Comment, Priority
from apps.forum.serializers import Forum_templateSerializers, ForumSerializers, CommentSerializers, \
    Parent_CommentSerializers, CommentSerializersAdd, ForumSerializers, Parent_CommentSerializersHelper
from apps.support.models import Seo
from apps.uitls.permissions import IsOwnerOr, IsOwnerOrReadOnly
from apps.user.models import UserMessage, User


# def get_online_count():
#     online_ips = cache.get("online_ips", [])
#     print(online_ips)
#     if online_ips:
#         #online_ips = cache.get_many(online_ips).keys()
#         return len(online_ips)
#     return 0


def index(request):
    """
    帖子首页
    :param request:
    :return:
    """
    #seo_list = get_object_or_404(Seo, name='社区论坛')
    plate = Forum_template.objects.all()
    forum = Forum.objects.filter(hidden=False).exclude(priority=Priority.objects.first())
    zd = Priority.objects.all()
    job = Forum.objects.filter(hidden=False,category__name='求职招聘')
    try:
        page = request.GET.get('page', 1)
        if page == '':
            page = 1
    except PageNotAnInteger:
        page = 1
        # Provide Paginator with the request object for complete querystring generation
    p = Paginator(forum, 10, request=request)
    people = p.page(page)
    return render(request,'pc/forum.html',locals())




@login_required(login_url='/login')
def indexMe(request):
    """
    我的帖子首页
    :param request:
    :return:
    """
    plate = Forum_template.objects.all()
    forum = Forum.objects.filter(hidden=False)
    follow_cnt = User.objects.filter(follow__fan__id=request.user.id).count()
    followed_cnt = User.objects.filter(fan__follow_id=request.user.id).count()
    try:
        page = request.GET.get('page', 1)
        if page == '':
            page = 1
    except PageNotAnInteger:
        page = 1
        # Provide Paginator with the request object for complete querystring generation
    p = Paginator(forum, 10, request=request)
    people = p.page(page)
    return render(request,'pc/forum_me.html',locals())


@login_required(login_url='/login')
def add_forum(request):
    """
    新增帖子
    :param request:
    :return:
    """
    category = Forum_template.objects.all()
    #seo_list = get_object_or_404(Seo, name='社区论坛')
    if request.method == 'POST':
        form = Forum_form(request.POST)
        if form.is_valid():
            forum = Forum()
            forum.title = form.cleaned_data.get('title')
            forum.category_id = form.cleaned_data.get('category')
            forum.keywords = request.POST.get('keywords')
            forum.content = form.cleaned_data.get('content')
            forum.author = form.cleaned_data.get('author')
            try:
                forum.save()
                return JsonResponse({"code": 200, "data": "发布成功"})
            except Exception as e:
                return JsonResponse({"code": 400, "data": "发布失败"})
        pattern = re.compile(r'<[^>]+>', re.S)
        result = pattern.sub("", str(form.errors))
        return JsonResponse({"code": 400, "data": result})
    return render(request,'pc/forum_add.html',locals())


@login_required(login_url='/login')
def update_forum(request,forum_id):
    if request.method == 'GET':
        item = get_object_or_404(Forum,pk=forum_id)
        plate = Forum_template.objects.all()
        #seos = get_object_or_404(Seo, name='社区论坛')
        return render(request,'pc/forum_update.html',{'plate':plate,'forum':item})
    elif request.method == 'POST':
        form = Forum_form(request.POST)
        if form.is_valid():
            forum = get_object_or_404(Forum,pk=forum_id)
            forum.title = form.cleaned_data.get('title')
            forum.category_id = form.cleaned_data.get('category')
            forum.keywords = request.POST.get('keywords')
            forum.content = form.cleaned_data.get('content')
            forum.author = form.cleaned_data.get('author')
            try:
                forum.save()
                return JsonResponse({"code": 200, "data": "修改成功"})
            except Exception:
                return JsonResponse({"code": 400, "data": "修改失败"})
        else:
            pattern = re.compile(r'<[^>]+>', re.S)
            result = pattern.sub("", str(form.errors))
            return JsonResponse({"code": 400, "data": result})


@login_required(login_url='/login')
def delForum(request,id):
    """
    删除帖子
    :param request:
    :param id:
    :return:
    """
    if request.is_ajax():
        try:
            data = get_object_or_404(Forum,pk=id)
            data.hidden=True
            data.save()
            return JsonResponse({'status':200,'message':'删除成功'})
        except Exception as e:
            return JsonResponse({'status': 400, 'message': '删除失败'})


def forum_category(request,category):
    """
    分类
    :param request:
    :param category:
    :return:
    """
    cate_list = Forum.objects.filter(category_id=category,hidden=False)
    plate = Forum_template.objects.all()

    job = Forum.objects.filter(hidden=False,category__name='求职招聘')
    type = get_object_or_404(Forum_template,pk=category)
    try:
        page = request.GET.get('page', 1)
        if page == '':
            page = 1
    except PageNotAnInteger:
        page = 1
        # Provide Paginator with the request object for complete querystring generation
    p = Paginator(cate_list, 20, request=request)
    people = p.page(page)

    return render(request,'pc/forum_category.html',locals())


def forum_detail(request,forum_id):
    """
    详情
    :param request:
    :param forum_id:
    :return:
    """
    dicts = get_object_or_404(Forum,pk=forum_id)
    dicts.click_nums+=1
    dicts.save()
    if request.method == 'POST':
        form = ParentComment(request.POST)
        if form.is_valid():
            try:
                data = Parent_Comment()
                data.forum = form.cleaned_data.get('forum')
                data.user = forms.cleaned_data.get('user')
                data.comment = form.cleaned_data.get('comment')
                data.parent_comment = form.cleaned_data.get('parent_comment')
                data.to_Parent_Comment = form.cleaned_data.get('to_Parent_Comment')
                data.url = forms.cleaned_data.get('url')
                data.address = request.POST.get('address')
                data.save()
                return JsonResponse({"code": 200, "data": "发布成功"})
            except Exception as e:
                return JsonResponse({"code": 400, "data": "发布失败"})
        else:
            pattern = re.compile(r'<[^>]+>', re.S)
            result = pattern.sub("", str(form.errors))
            return JsonResponse({"code": 400, "data": result})
    return render(request,'pc/forum_detail.html',{'dicts':dicts})


@receiver(post_save, sender=Parent_Comment)
def my_callback_reply(sender, **kwargs):
    """
    评论通知
    :param sender:
    :param kwargs:
    :return:
    """
    try:
        message = UserMessage()
        message.user_id = kwargs['instance'].to_Parent_Comments_id
        message.ids = kwargs['instance'].forums_id
        message.to_user_id = kwargs['instance'].user.id
        message.has_read = False
        message.url =kwargs['instance'].url
        message.message = "你参与的 %s 帖子评论有人回复了,快去看看吧!"%kwargs['instance'].parent_comments.forums.title
        message.save()
    except Exception as e:
        pass






class Forum_templateView(mixins.UpdateModelMixin,mixins.CreateModelMixin,viewsets.ReadOnlyModelViewSet):
    """TODO 版块分類"""
    queryset = Forum_template.objects.all()
    serializer_class = Forum_templateSerializers
    #permission_classes = (IsAuthenticated, IsOwnerOr)  # 未登录禁止访问
    authentication_classes = [JSONWebTokenAuthentication,SessionAuthentication]

    def get_permissions(self):
        if self.action == 'list':
            return []
        elif self.action == 'retrieve':
            return []
        else:
            return [IsAuthenticated(), IsOwnerOr()]

    #def put(self, request, pk, *args, **kwargs):
        #return self.update(request, *args, **kwargs)

    #def post(self, request, *args, **kwargs):
        #return self.create(request, *args, **kwargs)


class ForumView(viewsets.ModelViewSet):
    """TODO 帖子"""
    queryset = Forum.objects.all()
    serializer_class = ForumSerializers
    pagination_class = StandardResultsSetPagination
    #permission_classes = (IsAuthenticated, IsOwnerOr)  # 未登录禁止访问
    filter_backends = (DjangoFilterBackend,)
    filter_class = ForumFilter
    authentication_classes = [JSONWebTokenAuthentication,SessionAuthentication]

    def get_permissions(self):
        if self.action == 'list':
            return []
        elif self.action == 'retrieve':
            return []
        else:
            return [IsAuthenticated(), IsOwnerOr()]

    def get_queryset(self):
        user_id = self.request.query_params.get('pk')
        if user_id:
            return Forum.objects.filter(author_id=user_id, hidden=False)

        if self.request.user.is_superuser and self.request.user:
            return Forum.objects.all()
        elif self.request.user.is_active:
            return Forum.objects.filter(author=self.request.user,hidden=False)
        else:
            return Forum.objects.filter(hidden=False)


class ForumListView(viewsets.ReadOnlyModelViewSet):
    """TODO 帖子"""
    queryset = Forum.objects.filter(hidden=False)
    serializer_class = ForumSerializers
    pagination_class = StandardResultsSetPagination
    filter_backends = (DjangoFilterBackend,)
    filter_class = ForumFilter

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.click_nums+=1
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

class CommentView(mixins.CreateModelMixin,viewsets.ReadOnlyModelViewSet):

    """TODO 评论"""
    queryset = Comment.objects.all()
    #serializer_class = CommentSerializers
    #permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)  # 未登录禁止访问
    authentication_classes = [SessionAuthentication,JSONWebTokenAuthentication]

    def get_permissions(self):
        if self.action == 'list':
            return []
        elif self.action == 'retrieve':
            return []
        else:
            return [IsAuthenticated(), IsOwnerOrReadOnly()]

    def get_serializer_class(self):
        if self.action == 'list':
            return CommentSerializers
        elif self.action == 'retrieve':
            return CommentSerializers
        else:
            return CommentSerializersAdd



@receiver(post_save, sender=Comment)
def my_callback(sender, **kwargs):
    """
    评论通知
    :param sender:
    :param kwargs:
    :return:
    """
    message = UserMessage()
    message.user=kwargs['instance'].forum.author
    message.ids = kwargs['instance'].forum.id
    message.to_user_id = kwargs['instance'].user_id
    message.has_read = False
    message.url =kwargs['instance'].url
    message.message="你的%s帖子被人评论了,快去看看吧!"%kwargs['instance'].forum.title
    message.save()


class Parent_CommentView(mixins.CreateModelMixin,viewsets.ReadOnlyModelViewSet):

    """TODO 评论回复"""
    queryset = Parent_Comment.objects.all()
    serializer_class = Parent_CommentSerializersHelper
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)  # 未登录禁止访问
    authentication_classes = [SessionAuthentication,JSONWebTokenAuthentication]


@receiver(post_save, sender=Parent_Comment)
def my_callback_reply(sender, **kwargs):
    """
    评论通知
    :param sender:
    :param kwargs:
    :return:
    """
    message = UserMessage()

    message.user=kwargs['instance'].to_Parent_Comment
    message.ids = kwargs['instance'].forum.id
    message.to_user_id = kwargs['instance'].user_id
    message.has_read = False

    message.url =kwargs['instance'].url
    message.message="你参与的%s帖子评论有人回复了,快去看看吧!"%kwargs['instance'].forum.title
    message.save()