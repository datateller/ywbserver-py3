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
from jiaquan import *
from datetime import *
from jiaquan import *
from users.utils import *
from utils.serialization import *
from .models import *
import json, base64, traceback, random
import datetime,time


@csrf_exempt   ###保证对此接口的访问不需要csrf
def post_topic_webview(request, current_uid):
    userid = int(current_uid)
    user = User.objects.get(id=userid)
    if not user:
        return HttpResponse('INVALID_USER')
    content = request.POST.get('topic_content')
    if not content:
        return HttpResponseRedirect('/jiaquan/gettopicwebview/%s/' % current_uid)
    timenow = datetime.datetime.utcnow().replace(tzinfo=utc)
    topic = JiaTopic(from_user = user,
                 content =  content,
                 create_time = timenow,
                 update_time = timenow)
    ret = topic.save()
    topic_id = topic.id
    circle = user.circle
    circle.last_access = timenow # update the last-access time.
    circle.save()
    if topic_id and circle:
        circle.add_topic(topic)
        return HttpResponseRedirect('/jiaquan/topic/webview/%s/' % current_uid)
    else:
        return HttpResponse('POST_TOPIC_ERROR')

#webview方式展示一个用户的圈子里的所有帖子
def get_topic_webview(request, uid):
    userid = int(uid)
    user = User.objects.get(id=userid)
    if not user:
        print("##invalid user")
        return HttpResponse('INVALID_USER')
    timenow = datetime.datetime.utcnow().replace(tzinfo=utc)
    try:
      circle = user.circle
    except Exception as e:
      print("##get user circle exception:", e)
      return HttpResponse("请填写您所在位置，我们会为您创建圈子")
    circle.last_access = timenow # update the last-access time.
    circle.save()
    topicids = circle.topic_ids
    circletopics = []
    for topicid in reversed(topicids):
        topic = JiaTopic.objects.get(id = topicid)
        circletopics.append(topic)
    context = {}
    context['topics'] = circletopics
    context['current_uid'] = uid
    t = get_template("jiaquan/topics_webview.html") 
    return HttpResponse(t.render(Context(context)))


#根据topicid显示一个topic的详细信息webview
def get_topicbyid_webview(request, userid, topicid):
    try:
        topic = JiaTopic.objects.get(id = topicid)
        if not topic:
            return HttpResponse(json_serialize(status = 'EXCEPTION', result = 'INVALID_ID'))
    except Exception as e:
        return HttpResponse(json_serialize(status = 'EXCEPTION', result = 'INVALID_ID'))
    try:
        user = User.objects.get(id=userid)
        if not topic:
            return HttpResponse(json_serialize(status = 'EXCEPTION', result = 'INVALID_USERID'))
    except Exception as e:
            return HttpResponse(json_serialize(status = 'EXCEPTION', result = 'INVALID_USERID'))
    context = {}
    context['headurl'] = getheadurl(topic.from_user, 'thumbnail')
    context['topic'] = topic
    context['current_uid'] = userid
    t = get_template("jiaquan/topic_webview.html")
    return HttpResponse(t.render(Context(context)))


@csrf_exempt
def addcommentwebview(request, current_uid, topicid):
    userid = int(current_uid)
    user = User.objects.get(id=userid)
    if not user:
        return HttpResponse('INVALID_USER')
    topic = JiaTopic.objects.get(id=int(topicid))
    timenow = datetime.datetime.utcnow().replace(tzinfo=utc)
    JiaComment = JiaComment(from_user = user, topic=topic, content=request.POST['comment'], create_time=timenow)
    JiaComment.save()
    return HttpResponseRedirect('/jiaquan/topic/webview/%s/%s/' % (current_uid, topicid))


@csrf_exempt
def add_comment(request):
    (authed, username, password, user) = auth_user(request)
    timenow = datetime.datetime.utcnow().replace(tzinfo=utc)
    circle = user.circle
    if not circle:
        return HttpResponse('CIRCLE_NOT_FOUND_ERROR')
    circle.last_access = timenow # update the last-access time.
    circle.save()
    topicid = request.POST.get('topicid')
    if not topicid:
        return HttpResponse('TOPICID_NULL_ERROR')
    topic = JiaTopic.objects.get(id=int(topicid))
    if not topic:
        return HttpResponse('TOPIC_NOT_FOUND_ERROR')
    JiaComment = JiaComment(from_user = user, topic=topic, content=request.POST['comment'], create_time=timenow)
    JiaComment.save()
    if JiaComment:
        return HttpResponse('OK')
    else:
        return HttpResponse('ADD_COMMENT_ERROR')


def comments_encode(JiaComments):
    rets = []
    number = len(list(JiaComments))
    for i in range(0, number):
        JiaComment = JiaComments[i]
        c = {}
        c['from_user'] = JiaComment.from_user.username
        c['content'] = JiaComment.content
        c['create_time'] = JiaComment.create_time.strftime('%Y-%m-%d %H:%M:%S' )
        print(c)
        rets.append(c)
    return rets


def circletopiclist_encode(topics):
    rets = []
    number = len(list(topics))
    for i in range(0, number):
        topic = topics[i]
        t = {}
        t['topicid'] = topic.id
        t['from_user'] = topic.from_user.username
        t['headurl'] = getheadurl(topic.from_user, 'thumbnail')
        t['content'] = topic.content
        t['JiaComments_num'] = len(JiaComment.objects.filter(topic = topic))
        t['create_time'] = topic.create_time.strftime('%Y-%m-%d %H:%M:%S' )
        t['update_time'] = topic.update_time.strftime('%Y-%m-%d %H:%M:%S' )
        rets.append(t)
    #return json.dumps(rets, ensure_ascii=False)
    return rets


def circletopic_encode(topics):
    rets = []
    number = len(list(topics))
    for i in range(0, number):
        topic = topics[i]
        t = {}
        t['topicid'] = topic.id
        t['from_user'] = topic.from_user.username
        t['content'] = topic.content
        t['create_time'] = topic.create_time.strftime('%Y-%m-%d %H:%M:%S' )
        t['update_time'] = topic.update_time.strftime('%Y-%m-%d %H:%M:%S' )
        t['JiaComments'] = comments_encode(JiaComment.objects.filter(topic = topic))
        print(t)
        rets.append(t)
    return json.dumps(rets, ensure_ascii=False)


@csrf_exempt       
def get_circletopic(request):
    (authed, username, password, user) = auth_user(request)
    if not authed or not user:
        return HttpResponse(json_serialize(status = 'AUTH_FAILED'))
    timenow = datetime.datetime.utcnow().replace(tzinfo=utc)
    circle = user.circle
    if not circle:
        return HttpResponse(json_serialize(status = 'CIRCLE_NOT_EXIST'))
    circle.last_access = timenow # update the last-access time.
    circle.save()
    topicids = circle.topic_ids
    circletopics = []
    for topicid in reversed(topicids):
        topic = JiaTopic.objects.get(id = topicid)
        circletopics.append(topic)
    return HttpResponse(json_serialize(status = 'OK',result = circletopic_encode(circletopics)))


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
        topic = JiaTopic(from_user = user,
                     content =  content,
                     create_time = timenow,
                     update_time = timenow,
                     point = user.baby.homepoint)
        ret = topic.save()
        if  request.FILES and ('photo' in request.FILES.keys()) and request.FILES['photo'] != None:
            photo_data = request.FILES['photo']
            photo = Photo(topic = topic, photo_orig = photo_data)
            ret = photo.save()
        topic_id = topic.id
        circle = user.circle
        circle.last_access = timenow # update the last-access time.
        circle.save()
        if topic_id and circle:
            circle.add_topic(topic)
            return HttpResponse(json_serialize(status = 'OK'))
        else:
            return HttpResponse(json_serialize(status = 'EXCEPTION'), result = 'circle not found')
    except Exception as e:
        print('Exception:' + str(e))
        return HttpResponse(json_serialize(status = 'EXCEPTION', result = str(e)))


##获取帖子列表
def list_topic(request):
    try:
        if request.method == 'GET':
            return HttpResponse('HTTP_METHOD_ERR')
        (authed, username, password, user) = auth_user(request)
        if not authed or not user:
            return HttpResponse('AUTH_FAILED')
        timenow = datetime.datetime.utcnow().replace(tzinfo=utc)
        circle = user.circle
        if not circle:
            return HttpResponse('CIRCLE_NOT_EXIST')
        circle.last_access = timenow # update the last-access time.
        circle.save()
        topicids = circle.topic_ids
        circletopics = []
        for topicid in reversed(topicids):
            topic = JiaTopic.objects.get(id = topicid)
            circletopics.append(topic)
        return HttpResponse(circletopiclist_encode(circletopics))
    except Exception as e:
        return HttpResponse("EXCEPTION")


##获取帖子列表
def list_topic_nearby(request):
    try:
        if request.method != 'GET':
            return HttpResponse(json_serialize(status = 'HTTP_METHOD_ERR'))
        (authed, username, password, user) = auth_user(request)
        if not authed or not user:
            return HttpResponse(json_serialize(status = 'AUTH_FAILED'))
        #获取page参数
        if not request.GET.get('page'):
            page = 1
        else:
            page = int(request.GET.get('page'))
        #获取number参数
        if not request.GET.get('number'):
            number = 5
        else:
            number = int(request.GET.get('number'))
        paginator = None
        if not request.GET.get('longitude') or not request.GET.get('latitude'):
            paginator = get_nearby_point_topic(user.baby.homepoint, page_size = number)
        else:
            longitude = request.GET.get('longitude')
            latitude = request.GET.get('latitude')
            paginator = get_nearby_topic(longitude = longitude, latitude = latitude, page_size = number)
        try:
            return HttpResponse(json_serialize(status = 'OK', result = circletopiclist_encode(paginator.page(page))))
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            return HttpResponse(json_serialize(status = 'OK', result = circletopiclist_encode(paginator.page(paginator.num_pages))))
    except Exception as e:
        print('Exception' + str(e))
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
        comment = JiaComment(from_user = user,
                             content =  content,
                             create_time = timenow,
                             topic = JiaTopic.objects.get(id = topicid)
                             )

        ret = comment.save()
        return HttpResponse(json_serialize(status = 'OK'))
    except Exception as e:
        print('Exception:' + str(e))
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
            collection_record = JiaTopicCollection.objects.get(user = user)
        except JiaTopicCollection.DoesNotExist:
            new_collection_record = JiaTopicCollection(user = user, collections = [])
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
            collection_record = JiaTopicCollection.objects.get(user = user)
        except JiaTopicCollection.DoesNotExist:
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
            collection = user.jiatopiccollection
        except JiaTopicCollection.DoesNotExist:
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

