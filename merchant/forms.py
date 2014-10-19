'''
Created on 2013年12月31日

@author: shengeng
'''

from django import forms
from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import User 
from django.contrib import auth
from merchant.models import *
from commercial.models import *
import datetime

def validate_username(username):
    if User.objects.filter(username=username).exists():
        raise ValidationError(u'%s 已经被注册' % username)


class RegisterForm(forms.Form):

    email = forms.EmailField(validators=[validate_username],required=True,widget=forms.EmailInput(attrs={'placeholder':'请输入您的邮件地址' , ' class':'form-control','style':"width: 50%;",'autofocus':'autofocus','required':'required'}))
    name = forms.CharField(required=True,widget=forms.TextInput(attrs={'placeholder':'请输入您的商家名称', 'class':'form-control', 'required':'required'}))
    password = forms.CharField(required=True,widget=forms.PasswordInput(attrs={'placeholder':'请设置您到登录密码' , ' class':'form-control','style':"width: 50%;",'required':'required'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'请再次输入您的登录密码' , ' class':'form-control','style':"width: 50%;",'required':'required'}))
    city = forms.CharField(required=True,widget=forms.TextInput(attrs={'placeholder':'请输入您的城市' , ' class':'form-control','required':'required'}))
    address = forms.CharField(required=True,widget=forms.TextInput(attrs={'placeholder':'请输入您的具体地址' , ' class':'form-control','required':'required'}))
    longitude = forms.CharField(required=True,widget=forms.HiddenInput())
    latitude = forms.CharField(required=True,widget=forms.HiddenInput())
    description = forms.CharField(required=True,widget=forms.Textarea(attrs={'placeholder':'请输入关于您的商业描述' , ' class':'form-control','required':'required'}))
    agree = forms.NullBooleanField(widget=forms.CheckboxInput(attrs={'required':'required'}))
    
    def clean(self):
        cleaned_data = super(RegisterForm, self).clean()
        if cleaned_data['password'] != cleaned_data['password1']:
            self._errors["password1"] = self.error_class([u"密码不一致"])
            #del cleaned_data['password_again']
        return cleaned_data

class LoginForm(forms.Form):
    username = forms.CharField(required=True,widget=forms.TextInput(attrs={'placeholder':'用户名' , ' class':'form-control','required':'required','autofocus':'autofocus'}))
    password = forms.CharField(required=True,widget=forms.PasswordInput(attrs={'placeholder':'密码' , ' class':'form-control','required':'required'}))

    def clean(self):
        cleaned_data = super(LoginForm, self).clean()
        username = cleaned_data['username']
        password = cleaned_data['password']
        user = auth.authenticate(username=username, password=password)
        if user is None or not user.is_active:
            self._errors["username"] = self.error_class([u"用户认证失败"])
        return cleaned_data


class PostCommercialForm(forms.ModelForm):
    class Meta:
        model = Commercial
        fields = ('title', 'valid_date_from', 'valid_date_end', 'content', 'photo')
        widgets = {
            'title':forms.TextInput(attrs={'placeholder':'请输入您的标题' , ' class':'form-control','required':'required','autofocus':'autofocus'}),
            'content':forms.Textarea(attrs={'placeholder':'请输入您要发布的具体信息' , ' class':'form-control','required':'required'}), 
            #'valid_date_from':forms.TextInput(attrs={'placeholder':datetime.date.today().strftime("%m/%d/%Y"), 'class':'form-control', 'id':'validdatepicker_from', 'style':'width:40%; display:inline'}), 
            'valid_date_from':forms.TextInput(attrs={ 'class':'form-control', 'id':'validdatepicker_from', 'style':'width:40%; display:inline'}), 
            #'valid_date_from':forms.TextInput(attrs={'placeholder':datetime.date.today().strftime("%m/%d/%Y"), 'id':'validdatepicker_from', 'style':'height:34px;padding:6px 12px;font-size:14px;line-height:1.42857143;color:#555}), 
            #'valid_date_end':forms.TextInput(attrs={'class':'form-control', 'id':'validdatepicker_end'}) 
            'valid_date_end':forms.TextInput(attrs={'id':'validdatepicker_end', 'class':'form-control', 'style':'width:40%; display:inline'}) 

            #'valid_date':forms.TextInput(attrs={'placeholder':datetime.date.today().strftime("%m/%d/%Y"), 'id':'validdatepicker'}) 
            }

class UserDemandRespForm(forms.ModelForm):
    class Meta:
        model = UserDemandResp
        #fields = ('userdemand', 'respcontent', 'resp_time', 'resp_merchantuser_id')
        fields = ('respcontent',)
        widgets = {
            'respcontent':forms.Textarea(attrs={'placeholder':'请输入您的接单信息', 'class':'form-control', 'rows':1, 'required':'required'})
        }

 
class CommercialCommentRespForm(forms.ModelForm):
    class Meta:
        model = CommercialCommentResp
        #fields = ('userdemand', 'respcontent', 'resp_time', 'resp_merchantuser_id')
        fields = ('respcontent',)
        widgets = {
            'respcontent':forms.Textarea(attrs={'placeholder':'请输入您的回复信息', 'class':'form-control', 'rows':1, 'required':'required'})
        }

