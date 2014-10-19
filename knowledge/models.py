from django.db import models
from django.contrib.auth.models import User
import base64, json, random, math
import dbarray


class Knowledge(models.Model):
    title = models.CharField(max_length=1000)
    keyword = models.CharField(max_length=1000)
    abstract = models.TextField(max_length=1000)
    images = models.TextField(max_length=1000)
    content = models.TextField(max_length=50000)
    min = models.IntegerField()
    max = models.IntegerField()
    apply_sex = models.CharField(max_length=10)
    url = models.CharField(max_length=1000)

class KnowledgeCollection(models.Model):
    user = models.OneToOneField(User)
    collections = dbarray.IntegerArrayField()


def get_knowls_byage(age, number = 5):
    knowls = Knowledge.objects.filter(max__gte = age, min__lte = age)
    count = knowls.count()
    if number >= count:
        print('knowledge in age %d is not enough' % age)
        return list(Knowledge.objects.all()[:number])
    else:
        return random.sample(list(knowls), number)

def get_knowls_random(number = 5):
    knowls = Knowledge.objects.all()
    count = knowls.count()
    if number >= count:
        return list(Knowledge.objects.all()[:1])
    else:
        return random.sample(list(knowls), number)
    
def get_knowls_byids(ids):
    if not ids:
        return None
    knowls =Knowledge.objects.filter(id__in = ids)
    knowls_list = list(knowls)
    knowls_list.sort(key=lambda knowll: -ids.index(knowll.id))
    return knowls_list
