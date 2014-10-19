from django.db import models
import datetime
from django.utils.timezone import utc
from quan.models import *

# Create your models here.
class TLNews(models.Model):
    age = models.FloatField()
    keyword = models.TextField()
    title = models.TextField(unique=True)
    summary = models.TextField(null = True)
    text = models.TextField(null = True)
    piclink = models.TextField(null = True)
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
    newslist = TLNews.objects.filter(age = age).order_by('-published_time')
    if not newslist:
        news =TLNews.objects.all().order_by('-published_time')[0]
    else:
        news =newslist[0]
    return news


def get_news_byids(ids):
    if not ids:
        return None
    news = TLNews.objects.filter(id__in = ids)
    news_list = list(news)
    news_list.sort(key=lambda news: -ids.index(news.id))
    return news_list



class LocalNews(models.Model):
    city = models.TextField()
    keyword = models.TextField()
    title = models.TextField(unique=True)
    summary = models.TextField()
    link = models.TextField()
    published_time = models.DateTimeField(default=datetime.datetime.utcnow().replace(tzinfo=utc))
    create_time = models.DateTimeField(default=datetime.datetime.utcnow().replace(tzinfo=utc))


class LocalNewsKeyword(models.Model):
    word = models.TextField()
    city = models.TextField()


class LocalNewsComment(CommentBase):
    news = models.ForeignKey(LocalNews)


class LocalNewsPraise(PraiseBase):
    news = models.ForeignKey(LocalNews, related_name="LocalNewsPraiseNews")


class LocalNewsCollection(models.Model):
    user = models.OneToOneField(User)
    collections = dbarray.IntegerArrayField()


def get_localnews_bycity(city):
    if city == None:
        return None
    print(city)
    news =LocalNews.objects.filter(city = city).order_by('-published_time')[0]
    return news


def get_localnews_byids(ids):
    if not ids:
        return None
    news = LocalNews.objects.filter(id__in = ids)
    news_list = list(news)
    news_list.sort(key=lambda news: -ids.index(news.id))
    return news_list