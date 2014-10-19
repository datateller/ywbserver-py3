'''
Created on Nov 2, 2013

@author: shengeng
'''
from django.conf.urls import patterns, url

from .views import *

urlpatterns = patterns('',
    url(r'^refresh_tlquan_news', refresh_tlquan_news, name='refresh_tlquan_news'),
    url(r'^refresh_jiaquan_news', refresh_jiaquan_news, name='refresh_jiaquan_news'),
    url(r'^tlnews/webview/', tlnews_webview, name='tlnews_webview'),
)