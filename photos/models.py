from django.db import models
from imagekit.models import ImageSpecField
from pilkit.processors import ResizeToFill
from ywbserver import settings
import datetime
from django.utils.timezone import utc
# Create your models here.

class PhotoBase(models.Model):
    subdir = models.CharField(max_length=1024)
    photo_orig = models.ImageField(upload_to='photos/'+datetime.datetime.utcnow().replace(tzinfo=utc).strftime("%Y-%m-%d"))
    photo_thumbnail = ImageSpecField(source='photo_orig',
                                      processors=[ResizeToFill(100, 100)],
                                      format='JPEG',
                                      options={'quality': 60})
    class Meta:
      abstract=True
    

class Head(models.Model):
    username = models.TextField(max_length=500,null=True)
    head_orig = models.ImageField(upload_to='head',null=True,blank=True)
    head_thumbnail = ImageSpecField(source='head_orig',
                                      processors=[ResizeToFill(100, 100)],
                                      format='JPEG',
                                      options={'quality': 60})


def getheadurl(user, type):
    if not user:
#         full_url = ''.join([settings.DOMAIN, '/media/head/default.jpg'])
#         return full_url
        url = "/media/head/default.jpg"
        return url
    heads = Head.objects.filter(username = user.username)
    if len(heads) == 0:
#         full_url = ''.join([settings.DOMAIN, '/media/head/default.jpg'])
        url = "/media/head/default.jpg"
    else:
        head = list(heads)[-1]
        if type == 'orig':
#             full_url = ''.join([settings.DOMAIN, head.head_orig.url])
            url = head.head_orig.url
        if type == 'thumbnail':
#             full_url = ''.join([settings.DOMAIN, head.head_thumbnail.url])
            url = head.head_thumbnail.url
    return url


