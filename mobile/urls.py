'''
Created on Nov 2, 2013

@author: shengeng
'''
from django.conf.urls import patterns, url

from .views import *

urlpatterns = patterns('',
    url(r'^getdata/', mobile_view, name='mobile view'),
    url(r'^getknowledges/', mobile_view_knowledges, name='mobile view'),
    url(r'^getshops/', mobile_view_shops, name='mobile view'),
    url(r'^getconsumptions/', mobile_view_consumptions, name='mobile view'),
    url(r'^findhelp/', mobile_view_findhelp, name='mobile find help'),
)
