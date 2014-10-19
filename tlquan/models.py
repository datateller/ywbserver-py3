from django.db import models
from django.contrib.auth.models import User
from django.contrib.gis.db import models
from django.contrib.gis.geos import Point, fromstr
from django.contrib.gis.measure import D
from ywbserver.settings import *
import datetime, json, dbarray
from django.utils.timezone import utc
from photos.models import *
from quan.models import *
from rss.models import *
# Create your models here.
        

class TlTopic(TopicBase):
    age = models.IntegerField()


class TlComment(CommentBase):
    topic = models.ForeignKey(TlTopic)


class Photo(PhotoBase):
    topic = models.ForeignKey(TlTopic)
    

class TlPraise(PraiseBase):
    topic = models.ForeignKey(TlTopic, related_name="TlPraiseTopic")
    

class TlTopicCollection(models.Model):
    user = models.OneToOneField(User)
    collections = dbarray.IntegerArrayField()


def comments_encode(comments):
    rets = []
    number = len(list(comments))
    for i in range(0, number):
        comment = comments[i]
        c = {}
        c['from_user'] = comment.from_user.username
        c['content'] = comment.content
        c['create_time'] = comment.create_time.strftime('%Y-%m-%d %H:%M:%S' )
        print(c)
        rets.append(c)
    return rets


def circletopiclist_encode(topics):
    rets = []
    number = len(list(topics))
    for i in range(0, number):
        topic = topics[i]
        t = {}
        t['topicid'] = topic.id
        if topic.from_user:
            t['from_user'] = topic.from_user.username
        else:
            t['from_user'] = "匿名用户"
        t['from_user_id'] = topic.from_user.id
        t['headurl'] = getheadurl(topic.from_user, 'thumbnail')
        t['content'] = topic.content
        t['comments_num'] = len(TlComment.objects.filter(topic = topic))
        t['create_time'] = topic.create_time.strftime('%Y-%m-%d %H:%M:%S' )
        t['update_time'] = topic.update_time.strftime('%Y-%m-%d %H:%M:%S' )
        t['link'] = ""
        rets.append(t)
    return rets


def circletopic_encode(topics):
    rets = []
    number = len(list(topics))
    for i in range(0, number):
        topic = topics[i]
        t = {}
        t['topicid'] = topic.id
        t['from_user'] = topic.from_user.username
        t['content'] = topic.content
        t['create_time'] = topic.create_time.strftime('%Y-%m-%d %H:%M:%S' )
        t['update_time'] = topic.update_time.strftime('%Y-%m-%d %H:%M:%S' )
        t['comments'] = comments_encode(TlComment.objects.filter(topic = topic))
        print(t)
        rets.append(t)
    return rets

#序列化圈子新闻
def circlenews_encode(news):
    t = {}
    t['topicid'] = -news.id
    t['from_user'] = "养娃宝新闻精选"
    t['from_user_id'] = 0
    t['headurl'] = getheadurl(None, 'thumbnail')
    t['content'] = news.text
    t['comments_num'] = 0
    t['create_time'] = news.create_time.strftime('%Y-%m-%d %H:%M:%S' )
    t['update_time'] = news.published_time.strftime('%Y-%m-%d %H:%M:%S' )
    t['link'] = DOMAIN + '/rss/tlnews/webview/?id=' + str(-news.id)
    return t
    
    #序列化圈子新闻
def circlenewslist_encode(newslist):
    rets = []
    number = len(list(newslist))
    for i in range(0, number):
        news = newslist[i]
        t = {}
        t['topicid'] = -news.id
        t['from_user'] = "养娃宝新闻精选"
        t['from_user_id'] = 0
        t['headurl'] = getheadurl(None, 'thumbnail')
        t['content'] = news.title
        t['comments_num'] = 0
        t['create_time'] = news.create_time.strftime('%Y-%m-%d %H:%M:%S' )
        t['update_time'] = news.published_time.strftime('%Y-%m-%d %H:%M:%S' )
        t['link'] = news.link
        rets.append(t)
    return rets
    
def get_topics_byids(ids):
    if not ids:
        return None
    topics =TlTopic.objects.filter(id__in = ids)
    topics_list = list(topics)
    topics_list.sort(key=lambda topics: -ids.index(topics.id))
    return topics_list
