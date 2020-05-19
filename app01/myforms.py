#! /usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = "Sunny"
# Date: 2020-05-12
from django import forms
from django.forms import widgets
from django.core.exceptions import ValidationError
from app01.models import  UserInfo
from django.contrib import auth

class Sell_bookForm(forms.Form):
    title = forms.CharField(
        max_length=32,label='书名',
        widget=widgets.Input(attrs={'class': 'form-control input-group input-group-lg'}),
        error_messages={'required':'必填项，不能为空'}
    )

    price = forms.FloatField(
        label='价格',
        widget=widgets.Input(attrs={'class': 'form-control'}),
        error_messages={'required':'必填项，不能为空'}
    )

    author = forms.CharField(
        label='作者',
        widget=widgets.Input(attrs={'class': 'form-control'}),
        error_messages={'required':'必填项，不能为空'}
    )
    publish = forms.CharField(
        label='出版社',
        widget=widgets.Input(attrs={'class': 'form-control'}),
        error_messages={'required':'必填项，不能为空'}
    )
    brief = forms.CharField(
        label='简介',
        widget=widgets.Input(attrs={'class': 'form-control'}),
        error_messages={'required':'必填项，不能为空'}
    )
    
    
    
    pub_time = forms.DateField(
        label='出版时间',
        widget=widgets.DateInput(attrs={'class': 'form-control','type': 'date'}),
        error_messages={'required':'必填项，不能为空'}
    )

class UserForm(forms.Form):
    name = forms.CharField(
        max_length=32,label='账号',
        widget=widgets.Input(attrs={'class': 'form-control input-group input-group-lg'}),
    )

    pwd = forms.CharField(
        max_length=32,label='密码',
        widget=widgets.Input(attrs={'class': 'form-control input-group input-group-lg'}),
    )

    re_pwd = forms.CharField(
        max_length=32,label='确认密码',
        widget=widgets.Input(attrs={'class': 'form-control input-group input-group-lg'}),
    )
    def clean(self):
        name =self.cleaned_data.get('name')
        user_obj = UserInfo.objects.filter(username=name).first()

        pwd=self.cleaned_data.get("pwd")
        re_pwd=self.cleaned_data.get("re_pwd")

        if user_obj:
            raise ValidationError("用户名已存在")
        elif pwd != re_pwd:
            raise ValidationError("两次密码不一致")
        else:
            return self.cleaned_data


class LoginForm(forms.Form):

    name = forms.CharField(
        max_length=32,label='账号',
        widget=widgets.Input(attrs={'class': 'form-control input-group input-group-lg'}),
    )

    pwd = forms.CharField(
        max_length=32,label='密码',
        widget=widgets.Input(attrs={'class': 'form-control input-group input-group-lg'}),
    )
    def clean(self):
        name=self.cleaned_data.get('name')
        pwd=self.cleaned_data.get('pwd')
        print(name,pwd)
        user_obj = auth.authenticate(username=name,password=pwd)
        print(user_obj)
        if user_obj:

            return self.cleaned_data
        else:
            raise ValidationError('用户名或者密码不正确')

