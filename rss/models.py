from django.db import models
import datetime
from django.utils.timezone import utc

# Create your models here.
class TLNews(models.Model):
    age = models.FloatField()
    keyword = models.TextField()
    title = models.TextField(unique=True)
    summary = models.TextField()
    link = models.TextField()
    published_time = models.DateTimeField(default=datetime.datetime.utcnow().replace(tzinfo=utc))
    create_time = models.DateTimeField(default=datetime.datetime.utcnow().replace(tzinfo=utc))


class TLNewsKeyword(models.Model):
    word = models.TextField()
    age = models.FloatField()

def get_news_byage(age):
    if not age:
        return None
    news =TLNews.objects.filter(age = age).order_by('-published_time')[0]
    return news
