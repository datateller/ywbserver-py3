from django.shortcuts import render
from django.http import *
from baby.models import Baby
from knowledge.models import *
from shop.models import *
from consumption.models import *
from django.contrib import auth
from django.contrib.auth.models import User
from django.utils import http
from django.core import serializers
from datetime import *
from users.utils import *
from merchant.models import *
import base64, json, random, math
from django.template.loader import get_template
from django.template import Context
from ywbserver.settings import *

def getknowllist(baby, number):
    if(baby and baby.birthday):
        age= (int((date.today() - baby.birthday).days))
        response = knowledge_list_encode(get_knowls_byage(age, number))
    else:
        response = knowledge_list_encode(get_knowls_random(number))
    return response

def getshoplist(baby, number):
    respones = None
    if(baby.homepoint):
        latitude = baby.homepoint.y
        longitude = baby.homepoint.x
        response = shop_list_encode(get_shop_nearby(latitude, longitude, number))
    else:
        response = shop_list_encode(get_shop_random(number))
    return response

def getconsumptionlist(baby, number):
    respones = None
    commercial_nearby = None
    if(baby.homepoint):
        commercial_nearby = get_commercial_nearby(baby.homepoint, number)
        response = consumption_list_encode(commercial_nearby)
    else:
        commercial_nearby = get_commercial_random(number)
        response = consumption_list_encode(commercial_nearby)
    
    for commercial in commercial_nearby:
        print("##commercialid:", commercial.id, "##merchantid:", commercial.merchant.id, "##babyid:", baby.id)
        store_commercial_history(commercial.id, commercial.merchant.id, baby.id) 

    return response

def getknowllist_anonymous(request, number):
    if not request.POST.get('age'):
        return HttpResponse('PARAMETER_NULL_AGE')
    age = int(request.POST.get('age'))
    response = knowledge_list_encode(get_knowls_byage(age, number))
    return response

def getshoplist_anonymous(request, number):
    response = shop_list_encode(get_shop_random(number))
    return response

def getconsumptionlist_anonymous(request, number):
    response = consumption_list_encode(get_commercial_random(number))
    return response

from django.views.decorators.csrf import csrf_exempt
@csrf_exempt
def mobile_view(request):
    (authed, username, password, user) = auth_user(request)
    if not authed or not user:
        return HttpResponse('AUTH_FAILED')
    knumber = int(request.POST.get('knumber'))
    snumber = int(request.POST.get('snumber'))
    cnumber = int(request.POST.get('cnumber'))
    if knumber == None or snumber == None or cnumber == None:
        return HttpResponse('PARAMETER_NULL_number')
    if user.username == 'anonymous':
        knowls = getknowllist_anonymous(request, knumber)
        shops = getshoplist_anonymous(request, snumber)
        consumptions = getconsumptionlist_anonymous(request, cnumber)
        return HttpResponse(data_encode(knowls, shops, consumptions))
    else:
        baby = Baby.objects.get(user=user)
        if not baby:
            return HttpResponse('BABY_DATA_NULL')
        knowls = getknowllist(baby, knumber)
        shops = getshoplist(baby, snumber)
        consumptions = getconsumptionlist(baby, cnumber)
        return HttpResponse(data_encode(knowls, getshoplist, consumptions))

@csrf_exempt
def mobile_view_knowledges(request):
    (authed, username, password, user) = auth_user(request)
    if not authed or not user:
        return HttpResponse('AUTH_FAILED')
    knumber = int(request.POST.get('knumber'))
    if knumber == None:
        return HttpResponse('PARAMETER_NULL_number')
    if user.username == 'anonymous':
        print("##anonymous user")
        knowls = getknowllist_anonymous(request, knumber)
        return HttpResponse(json.dumps(knowls, ensure_ascii=False))
    else:
        baby = Baby.objects.get(user=user)
        knowls = getknowllist(baby, knumber)
        return HttpResponse(json.dumps(knowls, ensure_ascii=False)) 

@csrf_exempt
def mobile_view_shops(request):
    (authed, username, password, user) = auth_user(request)
    if not authed or not user:
        return HttpResponse('AUTH_FAILED')
    snumber = int(request.POST.get('snumber'))
    if snumber == None:
        return HttpResponse('PARAMETER_NULL_number')
    if user.username == 'anonymous':
        shops = getshoplist_anonymous(request, snumber)
        return HttpResponse(json.dumps(shops, ensure_ascii=False))
        #return HttpResponse(data_encode(shops))
    else:
        baby = Baby.objects.get(user=user)
        if not baby:
            return HttpResponse('BABY_DATA_NULL')
        shops = getshoplist(baby, snumber)
        return HttpResponse(json.dumps(shops, ensure_ascii=False))
        #return HttpResponse(data_encode(shops))    

@csrf_exempt
def mobile_view_consumptions(request):
    (authed, username, password, user) = auth_user(request)
    if not authed or not user:
        return HttpResponse('AUTH_FAILED')
    cnumber = int(request.POST.get('cnumber'))
    if  cnumber == None:
        return HttpResponse('PARAMETER_NULL_number')
    if user.username == 'anonymous':
        consumptions = getconsumptionlist_anonymous(request, cnumber)
        return HttpResponse(json.dumps(consumptions, ensure_ascii=False))
        #return HttpResponse(data_encode(consumptions))
    else:
        baby = Baby.objects.get(user=user)
        if not baby:
            return HttpResponse('BABY_DATA_NULL')
        consumptions = getconsumptionlist(baby, cnumber)
        return HttpResponse(json.dumps(consumptions, ensure_ascii=False))
        #return HttpResponse(data_encode(consumptions))

def data_encode(*data_array):
    rets =''
    for (data) in data_array:
      rets = ('%s%s') % (rets, data)
    return json.dumps(rets, ensure_ascii=False)
    
def knowledge_list_encode(knowls):
    rets = []
    number = len(list(knowls))
    picindexes = random.sample((0,1,2,3,4,5,6,7,8,9), number)
    for i in range(0, number):
        knowl = knowls[i]
        t = {}
        tags = knowl.keyword.split(';')
        t['id'] = knowl.id
        t['title'] = knowl.title
        t['pic'] = 'http://www.yangwabao.com:8001/pic/'+str(picindexes[i])+'.jpg'
        t['icon'] = 'http://www.yangwabao.com:8001/icon/'+str(picindexes[i])+'.png'
        if knowl.abstract:
            t['Abstract'] = knowl.abstract
        else:
            t['Abstract'] = " "
        t['address'] = ""
        t['link'] = DOMAIN + ("/knowledge/webview/%d/" % knowl.id)
        rets.append(t)
    return rets

def shop_list_encode(shops):
    rets = []
    number = len(list(shops))
    picindexes = random.sample((0,1,2,3,4,5,6,7,8,9), number)
    for i in range(0, number):
        shop = shops[i]
        t = {}
        t['id'] = shop.id
        t['title'] = shop.name
        t['pic'] = 'http://www.yangwabao.com:8001/pic/'+str(picindexes[i])+'.jpg'
        t['icon'] = 'http://www.yangwabao.com:8001/icon/'+str(picindexes[i])+'.png'
#         if shop.abstract:
#             t['Abstract'] = shop.abstract
#         else:
#             t['Abstract'] = " "
        t['Abstract'] = shop.description
        t['address'] = shop.address
        t['link'] = DOMAIN + ("/shop/webview/%d/" % shop.id)
        rets.append(t)
    return rets

# def consumption_list_encode(consumptions):
#     rets = []
#     number = len(list(consumptions))
#     picindexes = random.sample((0,1,2,3,4,5,6,7,8,9), number)
#     for i in range(0, number):
#         consumption = consumptions[i]
#         t = {}
#         t['id'] = consumption.id
#         t['title'] = consumption.name
#         t['pic'] = 'http://www.yangwabao.com:8001/pic/'+str(picindexes[i])+'.jpg'
#         t['icon'] = 'http://www.yangwabao.com:8001/icon/'+str(picindexes[i])+'.png'
#         if consumption.abstract:
#             t['Abstract'] = consumption.abstract
#         else:
#             t['Abstract'] = " "
#         t['address'] = consumption.address
#         t['link'] = DOMAIN + ("/consumption/webview/%d/" % consumption.id)
#         rets.append(t)
#     return rets


def consumption_list_encode(consumptions):
    rets = []
    number = len(list(consumptions))
    picindexes = random.sample((0,1,2,3,4,5,6,7,8,9), number)
    for i in range(0, number):
        consumption = consumptions[i]
        t = {}
        t['id'] = consumption.id
        t['title'] = consumption.title
        t['pic'] = 'http://www.yangwabao.com:8001/pic/'+str(picindexes[i])+'.jpg'
        t['icon'] = 'http://www.yangwabao.com:8001/icon/'+str(picindexes[i])+'.png'
        t['Abstract'] = " "
        t['address'] = " "
        t['link'] = DOMAIN + ("/consumption/webview/%d/" % consumption.id)
        rets.append(t)
    return rets

from django.view.decorators.http import require_POST

@require_POST
def mobile_view_findhelp(request):
    (authed, username, password, user) = auth_user(request)
    if not authed or not user:
        return HttpResponse('AUTH_FAILED') 

    content = request.POST.get('content', '')
    pub_time = datetime.datetime.utcnow().replace(tzinfo=utc)
    userdemand = UserDemand(content=content, pub_time=pub_time)
    userdemand.save()
    return HttpResponse({'status':'OK'})

