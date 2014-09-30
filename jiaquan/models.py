from django.db import models
from django.contrib.auth.models import User
from django.contrib.gis.db import models as gis_models
from django.contrib.gis.geos import Point, fromstr
from django.contrib.gis.measure import D
from django.utils.timezone import utc
from django.core.paginator import Paginator, EmptyPage
from quan.models import *
from photos.models import *
from rss.models import *
import dbarray, json, datetime
# Create your models here.

class Circle(models.Model):
    user_source = models.IntegerField() # 1 is app user, 2 is weixinuser
    circle_users = dbarray.IntegerArrayField()
    point = gis_models.PointField()
    objects = gis_models.GeoManager()
    user = models.OneToOneField(User)
    topic_ids = dbarray.IntegerArrayField()
    last_access = models.DateTimeField(default=datetime.datetime.utcnow().replace(tzinfo=utc)) # recorde the last-access datatime
    not_deleted = models.BooleanField() # mark if this circle should be computed
    
    def add_topic(self, topic):
        self.topic_ids.append(topic.id)
        for notice_user_id in self.circle_users:
            notice_user = User.objects.get(id = notice_user_id)
            if not notice_user.circle.not_deleted:
                continue
            notice_user.circle.topic_ids.append(topic.id)
            notice_user.circle.save()
        self.save()
            
    def get_topics(self):
        pass


def create_circle(user, source, curpoint, distance=500000):
    try:
        incircles = Circle.objects.filter(point__distance_lt=(curpoint, D(km=int(distance) / 1000)))
        newcircleusers = []
        if incircles:
            for circle in incircles:
                circle.circle_users.append(user.id)
                circle.save()
                newcircleusers.append(circle.user.id)
        newcircle = Circle(user=user, user_source=source, circle_users=newcircleusers, point=curpoint, not_deleted=True, topic_ids=[])
        newcircle.save()
        return 'OK'
    except Exception as e:
        print(e)
        return 'ERROR'

def create_circle_from_position(user, source, longitude, latitude, distance=5000):
    point = fromstr("POINT(%s %s)" % (longitude, latitude))
    create_circle(user, source, point, distance)

def remove_circle(user, source):
    if not Circle.objects.filter(user = user):
        return 'OK'
    del_circle = user.circle
    if del_circle:
        for circle in Circle.objects.all():
            if circle.not_deleted:
                print(del_circle.user.id)
                if del_circle.user.id in circle.circle_users:
                    circle.circle_users.remove(del_circle.user.id)
                    circle.save()
        del_circle.delete()
        return 'OK'
        

class JiaTopic(TopicBase):
    point = gis_models.PointField()
    objects = gis_models.GeoManager()

class JiaComment(CommentBase):
    topic = models.ForeignKey(JiaTopic)
    class Meta:
        unique_together = ("topic", "from_user")
    
class JiaPraise(PraiseBase):
    topic = models.ForeignKey(JiaTopic, related_name="JiaPraiseTopic")
    
class Photo(PhotoBase):
    topic = models.ForeignKey(JiaTopic)

class JiaTopicCollection(models.Model):
    user = models.OneToOneField(User)
    collections = dbarray.IntegerArrayField()

def get_nearby_topic(longitude, latitude, page_size = 5, city = None):
    point = fromstr("POINT(%s %s)" % (longitude, latitude))
    topics = JiaTopic.objects.distance(point).order_by('distance')
    topics_list = list(topics)
    topics_list.sort(key=lambda topic:topic.update_time, reverse=True)
    rets = circletopiclist_encode(topics_list)
    newsret = circlenews_encode(get_localnews_bycity(city))
    if newsret:
        rets.insert(0, newsret)
    paginator = Paginator(rets, page_size)
    return paginator

def get_nearby_point_topic(point, page_size = 5, city = None):
    topics = JiaTopic.objects.distance(point).order_by('distance')
    topics_list = list(topics)
    topics_list.sort(key=lambda topic:topic.update_time, reverse=True)
    rets = circletopiclist_encode(topics_list)
    newsret = circlenews_encode(get_localnews_bycity(city))
    if newsret:
        rets.insert(0, newsret)
    paginator = Paginator(rets, page_size)
    return paginator


def comments_encode(JiaComments):
    rets = []
    number = len(list(JiaComments))
    for i in range(0, number):
        JiaComment = JiaComments[i]
        c = {}
        c['from_user'] = JiaComment.from_user.username
        c['content'] = JiaComment.content
        c['create_time'] = JiaComment.create_time.strftime('%Y-%m-%d %H:%M:%S' )
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
        t['headurl'] = getheadurl(topic.from_user, 'thumbnail')
        t['content'] = topic.content
        t['JiaComments_num'] = len(JiaComment.objects.filter(topic = topic))
        t['create_time'] = topic.create_time.strftime('%Y-%m-%d %H:%M:%S' )
        t['update_time'] = topic.update_time.strftime('%Y-%m-%d %H:%M:%S' )
        rets.append(t)
    #return json.dumps(rets, ensure_ascii=False)
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
        t['JiaComments'] = comments_encode(JiaComment.objects.filter(topic = topic))
        print(t)
        rets.append(t)
    return json.dumps(rets, ensure_ascii=False)


#序列化圈子新闻
def circlenews_encode(news):
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
    topics =JiaTopic.objects.filter(id__in = ids)
    topics_list = list(topics)
    topics_list.sort(key=lambda topics: -ids.index(topics.id))
    return topics_list