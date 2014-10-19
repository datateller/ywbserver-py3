from django.db import models
from django.contrib.gis.db import models
from django.contrib.auth.models import User
from django.contrib.gis.db import models
from django.contrib.gis.geos import Point, fromstr
from django.contrib.gis.measure import D
#from commercial.models import CommercialComment
import random
import dbarray
import datetime
from django.utils.timezone import utc
# Create your models here.

class Merchant(models.Model):
    user = models.OneToOneField(User)
    name = models.CharField(max_length=100)
    phonenumber = models.CharField(max_length=20)
    city = models.CharField(max_length=20)
    address = models.CharField(max_length=100)
    longitude = models.FloatField(null=True)
    latitude = models.FloatField(null=True)
    description = models.CharField(max_length=2000)
    point = models.PointField(null=True)
    objects = models.GeoManager()

    def geturl(self):
        return "http://www.yangwabao.com/merchant/merchantdetail/" + str(self.id) + "/"

class CommercialHistory(models.Model):
    commercial_id = models.IntegerField()
    merchant_id = models.IntegerField()
    baby_id = models.IntegerField()
    displaytime = models.DateTimeField()

class HelpFinder(models.Model):
    appuser_id = models.IntegerField()
    pub_time = models.DateTimeField()
    content = models.CharField(max_length=2000)

class UserDemand(models.Model):
    user = models.ForeignKey(User)
    content = models.CharField(max_length=2000)
    classify = models.CharField(max_length=15, null=True)
    validdate = models.DateTimeField(null=True)
    pub_time = models.DateTimeField()

    def getresp(self):
        return self.userdemandresp_set.all()

class UserDemandCollect(models.Model):
    user = models.OneToOneField(User)
    collections = dbarray.IntegerArrayField()

class UserDemandResp(models.Model):
    userdemand = models.ForeignKey(UserDemand)
    respcontent = models.CharField(max_length=1000)
    resp_time = models.DateTimeField()
    resp_merchantuser_id = models.IntegerField()


from commercial.models import CommercialComment
class CommercialCommentResp(models.Model):
    commercial_comment = models.ForeignKey(CommercialComment)
    respcontent = models.CharField(max_length=1000)
    resp_time = models.DateTimeField()
    resp_merchantuser_id = models.IntegerField()

def get_merchant_nearby(latitude, longitude, number=1, distance = 50000):
    point = fromstr("POINT(%s %s)" % (longitude, latitude))
    #nearby = Merchant.objects.using('ywbwebdb').filter(point__distance_lt=(point, D(km=int(distance)/1000)))
    nearby = Merchant.objects.filter(point__distance_lt=(point, D(km=int(distance)/1000)))
    count = nearby.count()
    if number >= count:
        print('appmerchant nearby %f,%f is not enough' % (latitude, longitude))
        return list(Merchant.objects.all()[:number-1])
    else:
        return random.sample(list(nearby), number)

def get_merchant_random(number=1):
    all = Merchant.objects.all()
    count = all.count()
    if number >= count:
        print('appmerchant random  is not enough')
        return list(all[:count])
    else:
        return random.sample(list(all), number)
    
def store_commercial_history(commercialid, merchantid, babyid):
    display_time = datetime.datetime.utcnow().replace(tzinfo=utc)
    commercialhistory = CommercialHistory(commercial_id=commercialid, merchant_id=merchantid, baby_id=babyid, displaytime=display_time)
    #commercialhistory.save(using="ywbwebdb") 
    commercialhistory.save() 

def userdemandslist_encode(userdemands):
    rets = []
    number = len(list(userdemands))
    for i in range(0, number):
        demand = userdemands[i]
        t = {}
        t['userdemand_userid'] = demand.user.id
        t['userdemand_id'] = demand.id
        t['content'] = demand.content
        t['publish_time'] = demand.pub_time.strftime('%Y-%m-%d %H:%M:%S') 
        respcount = demand.userdemandresp_set.count()
        t['response_state'] = 'yes' if respcount > 0 else 'no'
        t['response_num'] = respcount
        
        rets.append(t)
    return rets
