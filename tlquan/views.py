# Create your views here.
'''
Created on 2014.5.3

@author: shengeng
'''

from django.http import *
from baby.models import Baby
from django.contrib import auth
from django.contrib.auth.models import User
from django.utils import http
from django.contrib.gis.geos import Point, fromstr
from django.contrib.gis.measure import D # alias for Distance
from django.views.decorators.csrf import csrf_exempt
from django.template.loader import get_template
from django.template import Context
from django.utils.timezone import utc
from django.core.paginator import Paginator, EmptyPage
from jiaquan import *
from datetime import *
from users.utils import *
from utils.serialization import *
from photos.models import *
from .models import *
from rss.models import *
import json, base64, traceback, random, datetime, time


#根据topicid显示一个topic的详细信息webview
def topic_webview(request, userid, topicid):
    try:
        topic = TlTopic.objects.get(id = topicid)
        if not topic:
            return HttpResponse(json_serialize(status = 'INVALID_TOPICID'))
    except Exception as e:
        return HttpResponse(json_serialize(status = 'EXCEPTION'))
    try:
        user = User.objects.get(id=userid)
        if not topic:
            return HttpResponse(json_serialize(status = 'INVALID_USERID'))
    except Exception as e:
            return HttpResponse(json_serialize(status = 'EXCEPTION'))
    context = {}
    context['headurl'] = getheadurl(topic.from_user, 'thumbnail')
    context['topic'] = topic
    context['current_uid'] = userid
    t = get_template("tlquan/topic_webview.html")
    return HttpResponse(t.render(Context(context)))


@csrf_exempt
def addcommentwebview(request, current_uid, topicid):
    userid = int(current_uid)
    user = User.objects.get(id=userid)
    if not user:
        return HttpResponse(json_serialize(status = 'INVALID_USER'))
    topic = TlTopic.objects.get(id=int(topicid))
    timenow = datetime.datetime.utcnow().replace(tzinfo=utc)
    comment = TlComment(from_user = user, topic=topic, content=request.POST['comment'], create_time=timenow)
    comment.save()
    return HttpResponseRedirect('/tlquan/topic/webview/%s/%s/' % (current_uid, topicid))


@csrf_exempt   ###保证对此接口的访问不需要csrf
def post_topic(request):
    try:
        if request.method != 'POST':
            return HttpResponse(json_serialize(status = 'HTTP_METHOD_ERR'))
        (authed, username, password, user) = auth_user(request)
        if not authed or not user:
            return HttpResponse(json_serialize(status = 'AUTH_FAILED'))
        content = request.POST.get('content')
        if not content:
            return HttpResponse(json_serialize(status = 'CONTENT_NULL'))
        timenow = datetime.datetime.utcnow().replace(tzinfo=utc)
        age= (int((date.today().year - user.baby.birthday.year)))
        topic = TlTopic(from_user = user,
                     content =  content,
                     create_time = timenow,
                     update_time = timenow,
                     age = age)
        ret = topic.save()
        if  request.FILES and ('photo' in request.FILES.keys()) and request.FILES['photo'] != None:
            photo_data = request.FILES['photo']
            photo = Photo(topic = topic, photo_orig = photo_data)
            ret = photo.save()
        return HttpResponse(json_serialize(status = 'OK'))
    except Exception as e:
        print('Exception:' + str(e))
        return HttpResponse(json_serialize(status = 'EXCEPTION'))


##获取帖子列表
def list_topic(request):
    try:
        if request.method != 'GET':
            return HttpResponse(json_serialize(status = 'HTTP_METHOD_ERR'))
        (authed, username, password, user) = auth_user(request)
        if not authed or not user:
            return HttpResponse(json_serialize(status = 'AUTH_FAILED'))
        #获取page参数
        page = request.GET.get('page')
        if not page:
            page = 1
        else:
            page = int(page)
        #获取number参数
        number = request.GET.get('number')
        if not number:
            number = 5
        else:
            number = int(number)
        timenow = datetime.datetime.utcnow().replace(tzinfo=utc)
        baby = user.baby
        age= (int((date.today().year - user.baby.birthday.year)))
        topics = TlTopic.objects.filter(age = age)
        topics_list = list(topics)
        topics_list.sort(key=lambda topic:topic.update_time, reverse=True)
        paginator = Paginator(topics_list, number)
        newsret = circlenews_encode(get_news_byage(age))
        print(newsret)
        try:
            topicsret = circletopiclist_encode(paginator.page(page))
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            #return HttpResponse(json_serialize(status = 'OK', result = {'userid':user.id, 'topics':circletopiclist_encode(paginator.page(paginator.num_pages))}))
            topicsret = circletopiclist_encode(paginator.page(paginator.num_pages))
        finally:
            topicsret.insert(0, newsret)
            return HttpResponse(json_serialize(status = 'OK', result = {'topics':topicsret}))
    except Exception as e:
        print(str(e))
        traceback.print_exc()
        return HttpResponse(json_serialize(status = 'EXCEPTION'))


#发表评论接口，app native
@csrf_exempt   ###保证对此接口的访问不需要csrf
def post_comment(request):
    try:
        if request.method != 'POST':
            return HttpResponse(json_serialize(status = 'HTTP_METHOD_ERR'))
        (authed, username, password, user) = auth_user(request)
        if not authed or not user:
            return HttpResponse(json_serialize(status = 'AUTH_FAILED'))
        content = request.POST.get('content')
        topicid = request.POST.get('topicid')
        if not content:
            return HttpResponse(json_serialize(status = 'EXCEPTION'))
        if not topicid:
            return HttpResponse(json_serialize(status = 'EXCEPTION'))
        timenow = datetime.datetime.utcnow().replace(tzinfo=utc)
        comment = TlComment(from_user = user,
                             content =  content,
                             create_time = timenow,
                             topic = TlTopic.objects.get(id = topicid)
                             )

        ret = comment.save()
        return HttpResponse(json_serialize(status = 'OK'))
    except Exception as e:
        print('Exception:' + str(e))
        return HttpResponse(json_serialize(status = 'EXCEPTION', result = str(e)))

#点赞接口，app native
@csrf_exempt   ###保证对此接口的访问不需要csrf
def post_praise(request):
    try:
        if request.method != 'POST':
            return HttpResponse(json_serialize(status = 'HTTP_METHOD_ERR'))
        (authed, username, password, user) = auth_user(request)
        if not authed or not user:
            return HttpResponse(json_serialize(status = 'AUTH_FAILED'))
        topicid = request.POST.get('id')
        if not topicid:
            return HttpResponse(json_serialize(status = 'EXCEPTION'))
        timenow = datetime.datetime.utcnow().replace(tzinfo=utc)
        comment = TlPraise(from_user = user,
                             create_time = timenow,
                             topic = TlTopic.objects.get(id = topicid)
                             )
        ret = comment.save()
        return HttpResponse(json_serialize(status = 'OK'))
    except Exception as e:
        print('Exception:' + str(e))
        return HttpResponse(json_serialize(status = 'EXCEPTION', result = str(e)))

#取消赞接口，app native
@csrf_exempt   ###保证对此接口的访问不需要csrf
def cancel_praise(request):
    try:
        if request.method != 'POST':
            return HttpResponse(json_serialize(status = 'HTTP_METHOD_ERR'))
        (authed, username, password, user) = auth_user(request)
        if not authed or not user:
            return HttpResponse(json_serialize(status = 'AUTH_FAILED'))
        topicid = request.POST.get('id')
        if not topicid:
            return HttpResponse(json_serialize(status = 'EXCEPTION'))
        praise = TlPraise.objects.get(topic = TlTopic.objects.get(id = topicid), from_user = user)
        ret = praise.delete()
        return HttpResponse(json_serialize(status = 'OK'))
    except Exception as e:
        print('Exception:' + str(e))
        return HttpResponse(json_serialize(status = 'EXCEPTION', result = str(e)))


#列出赞过的帖子
def list_praise_topic(request):
    try:
        if request.method != 'GET':
            return HttpResponse(json_serialize(status = 'HTTP_METHOD_ERR'))
        (authed, username, password, user) = auth_user(request)
        if not authed or not user:
            return HttpResponse(json_serialize(status = 'AUTH_FAILED'))
        if not request.GET.get('page'):
            return HttpResponse(json_serialize(status = 'PARAM_NULL'))
        if not request.GET.get('number'):
            return HttpResponse(json_serialize(status = 'PARAM_NULL'))
        page = int(request.GET.get('page'))
        number = int(request.GET.get('number'))
        topics = TlTopic.objects.filter(TlPraiseTopic__from_user = user)
        paginator = Paginator(topics, number)
        try:
            return HttpResponse(json_serialize(status = 'OK', result = circletopiclist_encode(paginator.page(page))))
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            return HttpResponse(json_serialize(status = 'OK', result = circletopiclist_encode(paginator.page(paginator.num_pages))))
    except Exception as e:
        print('Exception:' + str(type(e)) + str(e))
        return HttpResponse(json_serialize(status = 'EXCEPTION', result = str(e)))


#收藏帖子
@csrf_exempt
def collect_topic(request):
    try:
        if request.method != 'POST':
            return HttpResponse(json_serialize(status = 'HTTP_METHOD_ERR'))
        (authed, username, password, user) = auth_user(request)
        if not authed or not user:
            return HttpResponse(json_serialize(status = 'PARAM_NULL'))
        if not request.POST.get('id'):
            return HttpResponse(json_serialize(status = 'PARAM_NULL'))
        topicid = request.POST.get('id')
        topicid = int(topicid)
        try:
            collection_record = TlTopicCollection.objects.get(user = user)
        except TlTopicCollection.DoesNotExist:
            new_collection_record = TlTopicCollection(user = user, collections = [])
            new_collection_record.collections.append(topicid)
            new_collection_record.save()
            return HttpResponse(json_serialize(status = 'OK'))
        else:
            if topicid not in collection_record.collections:
                collection_record.collections.append(topicid)
                collection_record.save()
            return HttpResponse(json_serialize(status = 'OK'))
    except Exception as e:
        print('Exception:' + str(e))
        return HttpResponse(json_serialize(status = 'EXCEPTION', result = str(e)))

#取消收藏
@csrf_exempt
def cancel_collection(request):
    try:
        if request.method != 'POST':
            return HttpResponse(json_serialize(status = 'HTTP_METHOD_ERR'))
        (authed, username, password, user) = auth_user(request)
        if not authed or not user:
            return HttpResponse(json_serialize(status = 'PARAM_NULL'))
        if not request.POST.get('id'):
            return HttpResponse(json_serialize(status = 'PARAM_NULL'))
        topicid = request.POST.get('id')
        topicid = int(topicid)
        try:
            collection_record = TlTopicCollection.objects.get(user = user)
        except TlTopicCollection.DoesNotExist:
            return HttpResponse(json_serialize(status='NOT_COLLECTED'))
        else:
            if topicid not in collection_record.collections:
                return HttpResponse(json_serialize(status='NOT_COLLECTED'))
            collection_record.collections.remove(topicid)
            collection_record.save()
            return HttpResponse(json_serialize(status = 'OK'))
    except Exception as e:
        print('Exception:' + str(e))
        return HttpResponse(json_serialize(status = 'EXCEPTION', result = str(e)))

#列出收藏
def list_collection(request):
    try:
        if request.method != 'GET':
            return HttpResponse(json_serialize(status = 'HTTP_METHOD_ERR'))
        (authed, username, password, user) = auth_user(request)
        if not authed or not user:
            return HttpResponse(json_serialize(status = 'AUTH_FAILED'))
        if not request.GET.get('page'):
            return HttpResponse(json_serialize(status = 'PARAM_NULL'))
        if not request.GET.get('number'):
            return HttpResponse(json_serialize(status = 'PARAM_NULL'))
        page = int(request.GET.get('page'))
        number = int(request.GET.get('number'))
        try:
            collection = user.tltopiccollection
        except TlTopicCollection.DoesNotExist:
            return HttpResponse(json_serialize(status = 'OK', result = {}))
        if not collection:
            return HttpResponse(json_serialize(status = 'OK', result = {}))
        topicids = collection.collections
        topics = get_topics_byids(topicids)
        paginator = Paginator(topics, number)
        try:
            return HttpResponse(json_serialize(status = 'OK', result = circletopiclist_encode(paginator.page(page))))
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            return HttpResponse(json_serialize(status = 'OK', result = circletopiclist_encode(paginator.page(paginator.num_pages))))
    except Exception as e:
        print('Exception:' + str(type(e)) + str(e))
        return HttpResponse(json_serialize(status = 'EXCEPTION', result = str(e)))
