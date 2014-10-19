# Create your views here.
'''
Created on Nov 2, 2013

@author: shengeng
'''

from django.http import *
from django.contrib import auth
from django.contrib.auth.models import User
from django.utils import http
from django.contrib.gis.geos import Point, fromstr
from django.contrib.gis.measure import D # alias for Distance
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate,login,logout  
from .models import *
from datetime import *
from .utils import *
import json, base64, traceback, random
import datetime, time, logging
from utils.baidumap import *
from baby.models import Baby
from jiaquan.models import *
from photos.models import *
from utils.serialization import *

log=logging.getLogger('customapp')

@csrf_exempt   ###保证对此接口的访问不需要csrf
def check_user_name(username):
    if User.objects.filter(username=username).exists():
        return "exist"
    else:
        return "available"

@csrf_exempt
def user_login(request):
    try:
        if request.method == "GET":
            return HttpResponse(json_serialize(status = 'HTTP_METHOD_ERR'))
        username = request.POST.get('username')
        password = request.POST.get('password')
        print("user login username base64 is :" + username)
        username = http.urlsafe_base64_decode(username)
        password = http.urlsafe_base64_decode(password)
        username = username.decode()
        password = password.decode()
        user = authenticate(username=username, password=password)
        if user is not None:  
            login(request, user)
            print("##success login")
            return HttpResponse(json_serialize(status = 'OK'))
        else: 
            print("##auth failed") 
            return HttpResponse(json_serialize(status = 'AUTH_FAILED'))
    except Exception as e:
        log.error(e)
        return HttpResponse(json_serialize(status = 'EXCEPTION'))
  
@csrf_exempt
def user_logout(request):
    try:
        if request.method != "POST":
            return HttpResponse(json_serialize(status = 'HTTP_METHOD_ERR'))
        (authed, username, password, user) = auth_user(request)
        if not user or not authed:
             return HttpResponse(json_serialize(status = 'AUTH_FAILED'))
        logout(request)
        return HttpResponse(json_serialize(status = 'OK'))
    except Exception as e:
        log.error(e)
        return HttpResponse(json_serialize(status = 'EXCEPTION'))

@csrf_exempt
def register(request):
    try:
        if request.method != "POST":
            return HttpResponse(json_serialize(status = 'HTTP_METHOD_ERR'))
        username = request.POST.get('username')
        password = request.POST.get('password')
        username = http.urlsafe_base64_decode(username)
        password = http.urlsafe_base64_decode(password)
        username = username.decode()
        password = password.decode()
        if check_user_name(username) == "exist":
            return HttpResponse(json_serialize(status = 'DUMPLICATE_NAME'))
        log.debug('user register %s  %s ' , username, password)
        baby = Baby()
        baby_name = request.POST.get('babyname')
        baby_height = request.POST.get('babyheight')
        baby_weight = request.POST.get('babyweight')
        baby_birthday = request.POST.get('birthday')
        baby_sex = request.POST.get('babysex')
        baby_homeaddr = request.POST.get('homeaddr')
        baby_schooladdr = request.POST.get('schooladdr')
        homelng = request.POST.get('homelng')
        homelat = request.POST.get('homelat')
        schoollng = request.POST.get('schoollng')
        schoollat = request.POST.get('schoollat')
        baby_mobile = request.POST.get('mobile')
        baby.name = baby_name
        baby.height = baby_height
        baby.weight = baby_weight
        baby.mobile = baby_mobile
        try:
            baby.birthday = datetime.datetime.fromtimestamp(time.mktime(time.strptime(baby_birthday,"%Y-%m-%d")))
        except Exception as e:
            log.error(e)
            return HttpResponse(json_serialize(status = 'BIRTHDAY_FORMAT_ERR'))
        baby.sex = baby_sex
        baby.type = 1   ###这个注册用户来自app
        #get latitude and longitude from baidumap.and save as a geo point.
        need_circle = False
        try:
            if(homelng and homelat):
                baby.homepoint = fromstr("POINT(%s %s)" % (homelng, homelat))
                baby.city = get_baidu_city(homelng, homelat)
                baby.homeaddr = get_baidu_address(homelat, homelng)
            elif(baby_homeaddr):
                baiduresp = get_baidu_location(baby_homeaddr)
                if baiduresp['result']['location']['lng'] and baiduresp['result']['location']['lat']:
                    lng = baiduresp['result']['location']['lng']
                    lat = baiduresp['result']['location']['lat']
                    baby.homepoint = fromstr("POINT(%s %s)" % (lng, lat))
                    baby.city = get_baidu_city(lat, lng)
                    baby.homeaddr = baby_homeaddr
                    need_circle = True
                else:
                    baby.homepoint = None
                    baby.city = None
                    baby.homeaddr = None
            else:
                baby.homepoint = None
                baby.city = None
                baby.homeaddr = None
        except Exception as e:
            baby.homepoint = None
            baby.city = None
            baby.homeaddr = None
            log.error(e)
            return HttpResponse(json_serialize(status = 'HOMEADDR_FORMAT_ERR'))
        ##try to save the school address
        try:
            if(schoollng and schoollat):
                baby.schoolpoint = fromstr("POINT(%s %s)" % (schoollng, schoollat))
                baby.city = get_baidu_city(schoollng, schoollat)
                baby.schooladdr = get_baidu_address(homelat, homelng)
            elif(baby_schooladdr):
                baiduresp = get_baidu_location(baby_schooladdr)
                if baiduresp['result']['location']['lng'] and baiduresp['result']['location']['lat']:
                    lng = baiduresp['result']['location']['lng']
                    lat = baiduresp['result']['location']['lat']
                    baby.schooladdr = fromstr("POINT(%s %s)" % (lng, lat))
                    baby.schooladdr = baby_schooladdr
                    need_circle = True
                else:
                    baby.schooladdr = None
                    baby.schooladdr = None
            else:
                baby.schooladdr = None
                baby.schooladdr = None
        except Exception as e:
            baby.schooladdr = None
            baby.schooladdr = None
            log.error(e)
            return HttpResponse(json_serialize(status = 'SCHOOLADDR_FORMAT_ERR'))
        log.info('user register, add a new baby %s, birthday: %s' % (baby.name, baby.birthday.strftime("%Y-%m-%d")))
    # 产生一个新用户:
        user = User.objects.create_user(username = username, password = password)
        user.baby = baby
        user.save()
        baby.save()
        if baby is None:
            return HttpResponse(json_serialize(status = 'EXCEPTION'))
        else:
            if need_circle:
                print("##create circle for user " + user.username)
                create_circle(user, 1, baby.homepoint)
            return HttpResponse(json_serialize(status = 'OK'))
    except Exception as e:
        return HttpResponse(json_serialize(status = 'EXCEPTION'))

@csrf_exempt
def update(request):
    try:
        if request.method != "POST":
            return HttpResponse(json_serialize(status = "HTTP_METHOD_ERR", result = {}))
        (authed, username, password, user) = auth_user(request)
        if not authed or not user:
            return HttpResponse(json_serialize(status = "AUTH_FAILED", result = {}))
        baby_height = request.POST.get('babyheight')
        baby_weight = request.POST.get('babyweight')
        baby_birthday = request.POST.get('birthday')
        baby_sex = request.POST.get('babysex')
        baby_name = request.POST.get('babyname')
        baby_homeaddr = request.POST.get('homeaddr')
        baby_schooladdr = request.POST.get('schooladdr')
        homelng = request.POST.get('homelng')
        homelat = request.POST.get('homelat')
        schoollng = request.POST.get('schoollng')
        schoollat = request.POST.get('schoollat')
        baby_mobile = request.POST.get('mobile')
        baby = User.objects.get(id=user.id).baby
        if not baby:
            response = 'BABY_INFO_NULL'
            return HttpResponse(response)
        if baby_weight:
            baby.weight = float(baby_weight)
        if baby_height:
            baby.height = float(baby_height)
        if baby_mobile:
            baby.mobile = float(baby_mobile)
        try:
            if baby_birthday:
                baby.birthday = datetime.datetime.fromtimestamp(time.mktime(time.strptime(baby_birthday,"%Y-%m-%d")))
        except Exception as e:
            print(e)
            return HttpResponse(json_serialize(status = "BIRTHDAY_FORMAT_ERR", result = e))
        print('user update, update baby info %s, birthday: %s' % (baby.name, baby_birthday))
        if baby_sex:
            baby.sex = baby_sex
        if baby_name:
            baby.name = baby_name
        try:
            if(homelng and homelat):
                baby.homepoint = fromstr("POINT(%s %s)" % (homelng, homelat))
                baby.city = get_baidu_city(homelng, homelat)
                baby.homeaddr = get_baidu_address(homelat, homelng)
            elif(baby_homeaddr):
                baiduresp = get_baidu_location(baby_homeaddr)
                if baiduresp['result']['location']['lng'] and baiduresp['result']['location']['lat']:
                    lng = baiduresp['result']['location']['lng']
                    lat = baiduresp['result']['location']['lat']
                    baby.homepoint = fromstr("POINT(%s %s)" % (lng, lat))
                    baby.city = get_baidu_city(lat, lng)
                    baby.homeaddr = baby_homeaddr
                    print("##delete old circle")
                    if remove_circle(user, 1) != 'OK':
                        return HttpResponse(json_serialize(status = "UPDATE_CIRCLE_ERR", result = {}))
                    print("##re-create circle")
                    if create_circle(user, 1, baby.homepoint) != 'OK':
                        return HttpResponse(json_serialize(status = "CREATE_CIRCLE_ERR", result = {}))
                else:
                    return HttpResponse(json_serialize(status = "HOMEADDR_FORMAT_ERR", result = {}))
        except Exception as e:
            print(e)
            return HttpResponse(json_serialize(status = "HOMEADDR_FORMAT_EXCEPTION", result = {}))
        try:
            if(schoollng and schoollat):
                baby.schoolpoint = fromstr("POINT(%s %s)" % (schoollng, schoollat))
                baby.schooladdr = get_baidu_address(schoollat, schoollng)
            elif(baby_schooladdr):
                baiduresp = get_baidu_location(baby_schooladdr)
                if baiduresp['result']['location']['lng'] and baiduresp['result']['location']['lat']:
                    lng = baiduresp['result']['location']['lng']
                    lat = baiduresp['result']['location']['lat']
                    baby.schoolpoint = fromstr("POINT(%s %s)" % (lng, lat))
                    baby.schooladdr = baby_schooladdr
                else:
                    return HttpResponse(json_serialize(status = "SCHOOLADDR_FORMAT_ERR", result = {}))
        except Exception as e:
            print(e)
            return HttpResponse(json_serialize(status = "SCHOOLADDR_FORMAT_EXCEPTION", result = {}))
#         if baby_schooladdr:
#             baby.schooladdr = baby_schooladdr
        baby.save()
        response = 'False'
        if baby is None:
            return HttpResponse(json_serialize(status = "EXCEPTION", result = {}))
        else:
            return HttpResponse(json_serialize(status = "OK", result = {}))
    except Exception as e:
        print(e)
        return HttpResponse(json_serialize(status = "HTTP_METHOD_ERR", result = e))


@csrf_exempt
def getinfo(request):
    try:
        if request.method != "GET":
            return HttpResponse(json_serialize(status = "HTTP_METHOD_ERR", result = {}))
        (authed, username, password, user) = auth_user(request)
        if not user:
             return HttpResponse(json_serialize(status = "AUTH_FAILED", result = {}))
        else:
            baby = user.baby
            resp = {}
            resp['username'] = user.username
            resp['userid'] = user.id
            resp['babyname'] = baby.name
            resp['birthday'] = baby.birthday.strftime("%Y-%m-%d")
            resp['sex'] = baby.sex
            resp['weight'] = baby.weight
            resp['height'] = baby.height
            resp['city'] = baby.city
            resp['homeaddr'] = baby.homeaddr
            resp['schooladdr'] = baby.schooladdr
            return HttpResponse(json_serialize(status = "OK", result = resp))
    except Exception as e:
        print(e)
        return HttpResponse(json_serialize(status = "EXCEPTION", result = e))


@csrf_exempt
def upload_head(request):
    try :
        if request.method != 'POST':
            return HttpResponse(json_serialize(status = "HTTP_METHOD_ERR", result = {}))
        (authed, username, password, user) = auth_user(request)
        if not authed or not user:
            return HttpResponse(json_serialize(status = "AUTH_FAILED", result = {}))
        head_data = request.FILES['portrait']
        head = Head()
        head.username = user.username
        head.head_orig = head_data
        head.save()
        full_url = ''.join(['http://', request.META['HTTP_HOST'], head.head_thumbnail.url])
        print(full_url)
        return HttpResponse(json_serialize(status = "OK", result = full_url))
    except Exception as e:
        print('Exception:' + str(e))
        return HttpResponse(json_serialize(status = "EXCEPTION", result = e))
    
    
def get_head(request):
    try :
        if request.method != 'GET':
            return HttpResponse(json_serialize(status = "HTTP_METHOD_ERR", result = {}))
        (authed, username, password, user) = auth_user(request)
        if not authed or not user:
            return HttpResponse(json_serialize(status = "AUTH_FAILED", result = {}))
        type = 'thumbnail'
        if request.GET.get('type'):
            type = request.GET.get('type')
        if type == 'thumbnail':
            full_url = getheadurl(user = user, type = 'thumbnail')
        elif type == 'orig':
            full_url = getheadurl(user = user, type = 'orig')
#         elif type == 'custom':
#             if not request.GET.get('width') or not request.GET.get('height'):
#                 return HttpResponse(json_serialize(status = "INVALID_PARAM", result = {}))
#             else:
#                 width = int(request.GET.get('width'))
#                 height = int(request.GET.get('height'))
#                 full_url = getheadurl(user = user, type = 'custom', width = width, height = height)
#                 return HttpResponse(json_serialize(status = "OK", result = full_url))
        else:
            return HttpResponse(json_serialize(status = "INVALID_PARAM", result = {}))
        print(full_url)
        return HttpResponse(json_serialize(status = "OK", result = full_url))
    except Exception as e:
        print('Exception:' + str(e))
        return HttpResponse(json_serialize(status = "EXCEPTION", result = str(e)))


def gethomepic(request):
    try:
        (authed, username, password, user) = auth_user(request)
        if not user:
            return HttpResponse('AUTH_FAILED')
        else:
            piclink = "http://wjbb.cloudapp.net/homepic/%d.jpg"%random.randint(0,9)
            print(request.get_host())
            return HttpResponse(piclink)
    except Exception as e:
        print(e)
        return HttpResponse(e)
