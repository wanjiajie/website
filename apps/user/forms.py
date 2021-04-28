#!/usr/bin/python  
# -*- coding:utf-8 -*-  
from django import forms
from captcha.fields import CaptchaField

from apps.user.models import User, Follows


class CaptchaTestForm(forms.Form):

    captcha = CaptchaField()  # 验证码图片及输入框


class RegisterForm(forms.ModelForm):
    """注册"""
    password = forms.CharField(max_length=32)

    class Meta:
        model = User
        fields = ['username','email','password']

    def clean(self):
        clean = super(RegisterForm, self).clean()
        username=clean.get('username')
        password = clean.get('password')
        repeat = clean.get('repeat')
       # if password != repeat:
         #   self._errors['password'] = '前后输入密码不一致'
        return clean


class LoginForms(forms.Form):
    """登录"""
    telephone = forms.CharField()
    password = forms.CharField(max_length=16, min_length=9)
    remember = forms.BooleanField(required=False)

    def get_errors(self):
        if hasattr(self,'errors'):
            errors = self.errors.get_json_data()
            new_errors = {}
            for key,message_dicts in errors.items():
                messages = []
                for message in message_dicts:
                    messages.append(message['message'])
                new_errors[key] = messages
            return new_errors
        else:
            return {}


class ModifyForm(forms.Form):
    """修改密码"""
    password = forms.CharField(required=True)
    repeat = forms.CharField(required=True)
    email = forms.EmailField(required=True)

class EmailForm(forms.Form):
    """邮箱修改"""
    username = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    code = forms.CharField(required=True,max_length=4,min_length=4)


class InfoForm(forms.Form):
    username = forms.CharField(required=True)
    file = forms.ImageField(required=False)
    info = forms.CharField(required=False)
    position = forms.CharField(required=False)


class Follow_Forms(forms.ModelForm):

    class Meta:
        model = Follows
        fields = ['follow',]



