from django.shortcuts import render
import feedparser, urllib
# Create your views here.
from .models import *
from utils.serialization import *
from django.http import *
from django.db import transaction


@transaction.non_atomic_requests
def refresh_tlquan_news(request):
    keywords = TLNewsKeyword.objects.all()
    for keyword in keywords:
        age = keyword.age
        keywordsstr = keyword.word
        keywordsurl = urllib.parse.quote(keywordsstr)
        rssurl = "http://news.baidu.com/ns?word=title{0}&tn=newsrss&sr=0&cl=2&rn=20&ct=0".format(keywordsurl)
        d = feedparser.parse(rssurl)
        for entry in d.entries:
            published_time = datetime.datetime(*tuple(entry.published_parsed)[:6]).replace(tzinfo=utc)
            title = entry.title
            summary = entry.summary
            link = entry.links[0]['href']
            create_time = datetime.datetime.utcnow().replace(tzinfo=utc)
            news = TLNews(title = title,
                     age = age,
                     keyword =  keywordsstr,
                     create_time = create_time,
                     published_time = published_time,
                     summary = summary,
                     link = link)
            try:
                ret = news.save()
            except Exception as e:
                print('Exception:' + str(e))
            print(news.title)
    return HttpResponse(json_serialize(status = 'EXCEPTION'))


@transaction.non_atomic_requests
def refresh_jiaquan_news(request):
    keywords = LocalNewsKeyword.objects.all()
    for keyword in keywords:
        city = keyword.city
        keywordsstr = keyword.word
        keywordsurl = urllib.parse.quote(keywordsstr)
        rssurl = "http://news.baidu.com/ns?word=title{0}&tn=newsrss&sr=0&cl=2&rn=20&ct=0".format(keywordsurl)
        d = feedparser.parse(rssurl)
        for entry in d.entries:
            published_time = datetime.datetime(*tuple(entry.published_parsed)[:6]).replace(tzinfo=utc)
            title = entry.title
            summary = entry.summary
            link = entry.links[0]['href']
            create_time = datetime.datetime.utcnow().replace(tzinfo=utc)
            news = LocalNews(title = title,
                     city = city,
                     keyword =  keywordsstr,
                     create_time = create_time,
                     published_time = published_time,
                     summary = summary,
                     link = link)
            try:
                ret = news.save()
            except Exception as e:
                print('Exception:' + str(e))
            print(news.title)
    return HttpResponse(json_serialize(status = 'EXCEPTION'))
