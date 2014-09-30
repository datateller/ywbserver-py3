'''
Created on Nov 2, 2013

@author: shengeng
'''
from django.conf.urls import patterns, url

from .views import *

urlpatterns = patterns('',
    url(r'^posttopicwebview/(\d+)/$', post_topic_webview, name='post_topic_webview'),
    url(r'^gettopicwebview/([0-9]*)/$', get_topic_webview, name='get_topic_webview'),
    url(r'^topic/webview/(\d+)/(\d+)/$', get_topicbyid_webview, name='get_topicbyid_webview'),
    url(r'^addcommentwebview/(\d+)/(\d+)/$', addcommentwebview, name='addcommentwebview'),
    
    url(r'^postcomment/$', post_comment, name='post_comment'),
    url(r'^listcomment/$', list_comment, name='list_comment'),
    
    url(r'^posttopic/', post_topic, name='post_topic'),
    url(r'^listtopic/', list_topic, name='list_topic'),
    url(r'^listtopicnearby/', list_topic_nearby, name='list_topic_nearby'),
    
    url(r'^collect/',collect_topic, name='collectknowl'),
    url(r'^listcollect/',list_collection, name='list_collection'),
    url(r'^cancel/',cancel_collection, name='cancelknowl'),
    
    url(r'^postpraise/$', post_praise, name='post_praise'),
    url(r'^cancelpraise/$', cancel_praise, name='cancel_praise'),
    url(r'^listpraisetopic/$', list_praise_topic, name='list_praise_topic'),
)
