from django.db import models
from django.contrib.auth.models import User
from django.contrib.gis.db import models as gis_models
from django.contrib.gis.geos import Point, fromstr
from django.contrib.gis.measure import D
from django.utils.timezone import utc
from django.core.paginator import Paginator, EmptyPage
from quan.models import *
from photos.models import *
import dbarray
import datetime
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
    
class Photo(PhotoBase):
    topic = models.ForeignKey(JiaTopic)

def get_nearby_topic(longitude, latitude, page_size = 5):
    point = fromstr("POINT(%s %s)" % (longitude, latitude))
    topics = JiaTopic.objects.distance(point).order_by('distance')
    paginator = Paginator(topics, page_size)
    return paginator

def get_nearby_point_topic(point, page_size = 5):
    topics = JiaTopic.objects.distance(point).order_by('distance')
    paginator = Paginator(topics, page_size)
    return paginator