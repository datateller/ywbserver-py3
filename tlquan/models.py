from django.db import models
from django.contrib.auth.models import User
from django.contrib.gis.db import models
from django.contrib.gis.geos import Point, fromstr
from django.contrib.gis.measure import D
import datetime, json, dbarray
from django.utils.timezone import utc
from photos.models import *
from quan.models import *
# Create your models here.
        

class TlTopic(TopicBase):
    age = models.IntegerField()


class TlComment(CommentBase):
    topic = models.ForeignKey(TlTopic)


class Photo(PhotoBase):
    topic = models.ForeignKey(TlTopic)
    
    
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
        t['from_user'] = topic.from_user.username
        t['headurl'] = getheadurl(topic.from_user)
        t['content'] = topic.content
        t['comments_num'] = len(TlComment.objects.filter(topic = topic))
        t['create_time'] = topic.create_time.strftime('%Y-%m-%d %H:%M:%S' )
        t['update_time'] = topic.update_time.strftime('%Y-%m-%d %H:%M:%S' )
        rets.append(t)
    return json.dumps(rets, ensure_ascii=False)


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
    return json.dumps(rets, ensure_ascii=False)
    