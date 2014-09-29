from django.db import models
import datetime
from django.utils.timezone import utc
from quan.models import *

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


class TlNewsComment(CommentBase):
    news = models.ForeignKey(TLNews)


class TlNewsPraise(PraiseBase):
    news = models.ForeignKey(TLNews, related_name="TlNewsPraiseNews")


class TlNewsCollection(models.Model):
    user = models.OneToOneField(User)
    collections = dbarray.IntegerArrayField()


def get_news_byage(age):
    if age == None:
        return None
    news =TLNews.objects.filter(age = age).order_by('-published_time')[0]
    return news


def get_news_byids(ids):
    if not ids:
        return None
    news = TLNews.objects.filter(id__in = ids)
    news_list = list(news)
    news_list.sort(key=lambda news: -ids.index(news.id))
    return news_list

