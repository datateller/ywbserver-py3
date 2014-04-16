from django.db import models
from django.contrib.gis.db import models
from django.contrib.gis.geos import Point, fromstr
from django.contrib.gis.measure import D # alias for Distance
import random
# Create your models here.

class Consumption(models.Model):
    name = models.CharField(max_length=200)
    city = models.CharField(max_length=20)
    address = models.CharField(max_length=100)
    abstract = models.CharField(max_length=1000)
    description = models.CharField(max_length=5000)
    url = models.CharField(max_length=1000)
    begin = models.DateTimeField()
    end = models.DateTimeField()
    point = models.PointField()
    objects = models.GeoManager()

class EduConsumption(models.Model):
    pass

class EntertainConsumption(models.Model):
    pass

class ConsumptionComment(models.Model):
    consumptionid = models.ForeignKey(Consumption)
    comment = models.CharField(max_length=500)


def get_consumption_nearby(latitude, longitude, number=1, distance = 5000):
    point = fromstr("POINT(%s %s)" % (longitude, latitude))
    nearby = Consumption.objects.filter(point__distance_lt=(point, D(km=int(distance)/1000)))
    count = nearby.count()
    if number >= count:
        print('consumption nearby %f,%f is not enough' % (latitude, longitude))
        return list(Consumption.objects.all()[:number])
    else:
        return random.sample(list(nearby), number)

def get_consumption_random(number=1):
    all = Consumption.objects.all()
    count = all.count()
    if number >= count:
        print('consumption random  is not enough')
        return list(all[:count])
    else:
        return random.sample(list(all), number)
