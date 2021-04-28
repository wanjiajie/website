from datetime import datetime
import uuid
import os
from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

def user_directory_path(instance,filename):
    ext = filename.split('.')[-1]
    filename = '{}.{}'.format(uuid.uuid4().hex[:10],ext)
    # return the whole path to the file
    return os.path.join("user",instance.username,"avatar",filename)


class User(AbstractUser):

    #id = models.UUIDField(primary_key=True,default=uuid.uuid4)
    #name = models.CharField('姓名',max_length=30, blank=True, null=True)
    mobile = models.CharField('手机号',max_length=20,default='')
    position = models.CharField('职务',max_length=30,default='',null=True,blank=True)
    info = models.CharField('个人简介',max_length=100,default='',null=True,blank=True)
    avatar = models.ImageField(upload_to=user_directory_path,blank=True,null=True,default=None,verbose_name='用户头像')
   # user_avatar = models.URLField(default='',null=True,blank=True)
    email = models.EmailField(unique=True,default='')

    class Meta:
        verbose_name = "用户"
        verbose_name_plural = verbose_name

    def get_qq(self):
        if self.oauthqq_set.get(user=self):
            return True
        else:
            return False


class OAuthQQ(models.Model):
    """QQ"""
    id = models.UUIDField(primary_key=True,default=uuid.uuid4)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    #75247383A814E74901A95AA7D387142C
    nickname = models.CharField(max_length=100)
    qq_openid = models.CharField(max_length=100)
    figureurl_qq = models.URLField()


class Follows(models.Model):
    """关注表"""
    follow = models.ForeignKey(User,on_delete=models.CASCADE,related_name='follow',verbose_name='作者')
    fan = models.ForeignKey(User,on_delete=models.CASCADE,related_name='fan',verbose_name='粉丝')
    create_time = models.DateTimeField(auto_now_add=True,verbose_name='创建时间')

    def __str__(self):
        return str(self.follow.id)

    class Meta:
        verbose_name = '关注列表'
        verbose_name_plural = verbose_name
        ordering = ['-follow',]



class VerifyCode(models.Model):
    """邮箱验证码"""
    code = models.CharField(verbose_name='验证码',max_length=10)
    # mobile = models.CharField(blank=True,null=True,verbose_name='电话',max_length=11)
    # add_time = models.DateTimeField(default=datetime.now,verbose_name='添加时间')
    email = models.EmailField(verbose_name='邮箱',default='')
    send_choices = (
        ('register', '注册'),
        ('forget', '找回密码'),
        ('update_email', '修改邮箱')
    )
    send_type = models.CharField(verbose_name='验证码类型', max_length=30, choices=send_choices, default='register')

    send_time = models.DateTimeField(default=datetime.now, verbose_name='发送时间')

    def __str__(self):
        return self.code

    class Meta:
        verbose_name='邮箱验证码'
        verbose_name_plural=verbose_name


class UserMessage(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='user',verbose_name='收消息用户')
    to_user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='to_user',blank=True,null=True,verbose_name='发消息用户')
    message = models.TextField(verbose_name='消息内容')
    ids = models.UUIDField('评论文章id',blank=True,null=True)
    url = models.CharField('地址',max_length=200,blank=True,null=True)
    is_supper = models.BooleanField('系统消息',default=False)
    has_read = models.BooleanField('已读',default=False)
    create_time = models.DateTimeField(auto_now_add=True,verbose_name='创建时间',)

    def __str__(self):
        return self.message

    class Meta:
        verbose_name ='用户消息'
        verbose_name_plural=verbose_name
        ordering = ['-create_time',]

