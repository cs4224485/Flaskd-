# Author: harry.cai
# DATE: 2018/6/21
from django import forms
from django.forms import widgets
from Blog import models
from django.core.exceptions import ValidationError


class RegisterForm(forms.Form):
    '''
    注册form表单校验
    '''
    username = forms.CharField(
        max_length=32,
        error_messages={'required': '用户名不能为空'},
        widget=widgets.TextInput(attrs={'class': "form-control"}))
    password = forms.CharField(
        max_length=32,
        error_messages={'required': '密码不能为空'},
        widget=widgets.PasswordInput(attrs={'class': "form-control"}))
    re_pwd = forms.CharField(
        max_length=32,
        error_messages={'required': '密码不能为空'},
        widget=widgets.PasswordInput(attrs={'class': "form-control"}))

    email = forms.EmailField(
        error_messages={'required': '邮箱不能为空'},
        widget=widgets.EmailInput(attrs={'class': "form-control"}))
    check_code = forms.CharField(
        widget=widgets.TextInput(attrs={'class': "form-control"}))

    def clean_username(self):
        '''
        校验用户是否存在
        :return:
        '''
        username = self.cleaned_data.get('username')
        user_obj = models.UserInfo.objects.filter(username=username)
        if not user_obj:
            return username
        else:
            raise ValidationError('该用户已存在')

    def clean(self):
        '''
        校验两次输入的密码是否一致
        :return:
        '''
        password = self.cleaned_data.get('password')
        repwd = self.cleaned_data.get('re_pwd')
        if password == repwd:
            return self.cleaned_data
        else:
            raise ValidationError("两次密码输入不一致")

    def clean_email(self):
        '''
        校验注册邮箱是否已经注册
        :return:
        '''
        email = self.cleaned_data.get('email')
        user_obh = models.UserInfo.objects.filter(email=email)

        if not user_obh:
            return email
        else:
            raise ValidationError("该邮箱已被注册")


class EmailForm(forms.Form):
    '''
     获取邮箱注册验证码前对输入的邮箱进行校验
    '''

    email = forms.EmailField(
        error_messages={'required': '邮箱不能为空', "invalid": "邮箱格式错误"},
       )

    def clean_email(self):
        email = self.cleaned_data.get('email')
        user_obj = models.UserInfo.objects.filter(email=email)

        if not user_obj:
            return email
        else:
            raise ValidationError("该邮箱已被注册")
