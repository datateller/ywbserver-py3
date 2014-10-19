from django.db import models
from django.contrib.gis.db import models
from django.contrib.gis.geos import Point, fromstr
from django.contrib.gis.measure import D # alias for Distance
from django.utils.timezone import utc
from django.contrib.auth.models import User 
import random, datetime
from merchant.models import *
from ywbserver.settings import *
import datetime
# Create your models here.

# class commercial(models.Model):
#     name = models.CharField(max_length=5000)
#     city = models.CharField(max_length=20)
#     address = models.CharField(max_length=5000)
#     abstract = models.CharField(max_length=5000)
#     description = models.CharField(max_length=50000)
#     url = models.CharField(max_length=1000)
#     begin = models.DateTimeField()
#     end = models.DateTimeField()
#     point = models.PointField()
#     objects = models.GeoManager()
# 
# class commercialComment(models.Model):
#     commercialid = models.ForeignKey(commercial)
#     comment = models.CharField(max_length=500)


# def get_commercial_nearby(latitude, longitude, number=1, distance = 5000):
#     point = fromstr("POINT(%s %s)" % (longitude, latitude))
#     timenow = datetime.datetime.utcnow().replace(tzinfo=utc)
#     nearby = commercial.objects.filter(point__distance_lt=(point, D(km=int(distance)/1000)), end__gt=timenow)
#     count = nearby.count()
#     if number >= count:
#         print('commercial nearby %f,%f is not enough' % (latitude, longitude))
#         return list(commercial.objects.all()[:number])
#     else:
#         return random.sample(list(nearby), number)
#     
# def get_commercial_city(city, number=1, distance = 5000):
#     citystr = city.replace('市', '')
#     timenow = datetime.datetime.utcnow().replace(tzinfo=utc)
#     samecity = commercial.objects.filter(city__exact=citystr)
#     count = samecity.count()
#     if number >= count:
#         print('commercial in city %s is not enough' % (citystr))
#         return list(commercial.objects.all()[:number])
#     else:
#         return random.sample(list(samecity), number)
# 
# def get_commercial_random(number=1):
#     all = commercial.objects.all()
#     count = all.count()
#     if number >= count:
#         print('commercial random  is not enough')
#         return list(all[:count])
#     else:
#         return random.sample(list(all), number)


class Commercial(models.Model):
    merchant = models.ForeignKey(Merchant)
    title = models.CharField(max_length=100)
    content = models.CharField(max_length=20000)
    photo = models.ImageField(upload_to='b_photos/%Y/%m/%d', max_length=10000000, blank=True, null=True, default='b_photos/default.jpg')
    valid_date_from = models.DateField()
    #valid_date = models.DateField()
    valid_date_end = models.DateField(blank=True, null=True)
#     class Meta:
#         app_label="appmerchant"


class CommercialComment(models.Model):
    from_user = models.ForeignKey(User)
    commercialid = models.ForeignKey(Commercial)
    comment = models.CharField(max_length=5000)
    create_time = models.DateTimeField(default=datetime.datetime.utcnow().replace(tzinfo=utc))
    
    def getresp(self):
        print("###in commercial comment getresp")
        return self.commercialcommentresp_set.all()


class CommercialReceipt(models.Model):
    from_user = models.ForeignKey(User)
    commercial = models.ForeignKey(Commercial)
    receive_time = models.DateTimeField(default=datetime.datetime.utcnow().replace(tzinfo=utc))


def get_commercial_nearby(homepoint, number=1, distance = 50000):
    point = homepoint
    nearbym = Merchant.objects.filter(point__distance_lt=(point, D(km=int(distance)/1000)))
    count = nearbym.count()
    if number >= count:
        #merchants = Merchant.objects.using('ywbwebdb').all()[:number-1]
        merchants = nearbym
        commercials = []
        for merchant in merchants:
            commercial_set = Commercial.objects.filter(merchant = merchant)
            if len(commercial_set) >= 1:
                commercials.append(commercial_set[0])
        return commercials
    else:
        #merchants = Merchant.objects.using('ywbwebdb').all()[:number-1]
        merchants = nearbym
        merchants = random.sample(list(merchants), number)
        commercials = []
        for merchant in merchants:
            commercial_set = Commercial.objects.filter(merchant = merchant)
            if len(commercial_set) >= 1:
                commercials.append(commercial_set[0])
        return commercials


def get_commercial_random(number=1):
    all = Commercial.objects.all()
    count = all.count()
    if number >= count:
        return list(all[:count])
    else:
        return random.sample(list(all), number)
    

def commercial_list_encode(commercials):
    rets = []
    number = len(list(commercials))
    picindexes = random.sample((0,1,2,3,4,5,6,7,8,9), number)
    for i in range(0, number):
        commercial = commercials[i]
        t = {}
        t['id'] = commercial.id
        t['title'] = commercial.title
        t['pic'] = 'http://www.yangwabao.com:8001/pic/'+str(picindexes[i])+'.jpg'
        t['icon'] = 'http://www.yangwabao.com:8001/icon/'+str(picindexes[i])+'.png'
        t['address'] = commercial.merchant.address
        t['link'] = DOMAIN + ("/appcommercial/webview/%d/" % commercial.id)
        comentset = CommercialComment.objects.filter(commercialid=commercial.id)
        t['commentnum'] = str(len(comentset))
        rets.append(t)
    return rets

def getcommerciallist_anonymous(request, number):
    response = commercial_list_encode(get_commercial_random(number))
    return response

def getcommerciallist(baby, number):
    respones = None
    commercial_nearby = None
    if(baby.homepoint):
        commercial_nearby = get_commercial_nearby(baby.homepoint, number)
        response = commercial_list_encode(commercial_nearby)
    else:
        commercial_nearby = get_commercial_random(number)
        response = commercial_list_encode(commercial_nearby)
    for commercial in commercial_nearby:
        print("##commercialid:", commercial.id, "##merchantid:", commercial.merchant.id, "##babyid:", baby.id)
	#commen due to errors
        #store_commercial_history(commercial.id, commercial.merchant.id, baby.id)
    return response
    
