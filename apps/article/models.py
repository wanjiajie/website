import uuid
from datetime import datetime

import os
from django.db import models

from apps.user.models import User
# Create your models here.


class Category_Article(models.Model):
    """
    分类
    """
    name = models.CharField(max_length=100)
    order = models.IntegerField(default=0,verbose_name='排序')
    create_time = models.DateTimeField(auto_now_add=True)
    class Meta:
        verbose_name = '分类'
        verbose_name_plural = verbose_name


def article_directory_path(instance,filename):
    ext = filename.split('.')[-1]
    filename = '{}.{}'.format(uuid.uuid4().hex[:10],ext)
    # return the whole path to the file
    return os.path.join("article",instance.author.username,instance.title,filename)


class Article(models.Model):
    """
    文章
    """
    #id = models.UUIDField(default=uuid.uuid4,primary_key=True)
    author = models.ForeignKey(User,on_delete=models.CASCADE,verbose_name='用户')
    category = models.ForeignKey(Category_Article,on_delete=models.CASCADE,verbose_name='分类')
    title = models.CharField(max_length=100)
    keywords = models.CharField(max_length=200,blank=True,null=True)
    desc = models.CharField(max_length=256,blank=True,null=True)
    list_pic = models.ImageField(upload_to=article_directory_path,blank=True,null=True,default=None,verbose_name='列表图')
    content = models.TextField()
    click_nums = models.IntegerField(default=0,verbose_name='阅读数量')
    is_show = models.BooleanField(default=True,verbose_name='是否删除')
    create_time = models.DateTimeField(auto_now_add=True)

    def get_number(self):
        n= self.article_comment_set.all()
        num = self.article_comment_set.count()
        for i in n:
            num+=i.articlecommentreply_set.count()
        return num

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = '文章'
        verbose_name_plural = verbose_name
        ordering = ('-create_time',)


class Recommend(models.Model):
    recommends = models.ForeignKey(Article,on_delete=models.CASCADE,null=True,)
    is_recommend = models.BooleanField(default=False, verbose_name='是否推荐')
    create_time = models.DateTimeField(auto_now_add=True)
    class Meta:
        verbose_name = '文章推荐'
        verbose_name_plural = verbose_name
        ordering = ('-create_time',)


class Article_Comment(models.Model):
    """评论"""
    user = models.ForeignKey(User,on_delete=models.CASCADE,verbose_name='用户')
    article =models.ForeignKey(Article,verbose_name='文章',on_delete=models.CASCADE)
    content = models.TextField(verbose_name='评论')
    address = models.CharField(max_length=50,verbose_name='地址',blank=True,null=True)
    url = models.CharField(max_length=60, blank=True, null=True, default='')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='添加时间')

    def __str__(self):
        return self.article.title

    class Meta:
        verbose_name ='文章评论'
        verbose_name_plural=verbose_name
        ordering = ('-create_time',)


class ArticleCommentReply(models.Model):
    """评论回复"""
    user = models.ForeignKey(User,on_delete=models.CASCADE,verbose_name='当前用户',related_name='from_uid')
    to_uids = models.ForeignKey(User,on_delete=models.CASCADE,verbose_name='目标用户',related_name='to_uids',default='')
    comments = models.TextField(verbose_name='回复内容')
    url = models.CharField(max_length=60,blank=True,null=True,default='')
    comments_id = models.ForeignKey(Article_Comment,on_delete=models.CASCADE,verbose_name='回复id')
    address = models.CharField(max_length=50, verbose_name='地址',blank=True,null=True)
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='添加时间')


class Headlines(models.Model):
    """头条"""
    #id = models.UUIDField(default=uuid.uuid4,primary_key=True)
    title = models.CharField(max_length=200,verbose_name='标题')
    category = models.CharField(max_length=20,verbose_name='分类')
    content = models.TextField(verbose_name='内容',default='')
    author_name = models.CharField(max_length=100,verbose_name='来源')
    url = models.URLField(verbose_name='地址')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='添加时间')

    class Meta:
        ordering = ('-create_time',)