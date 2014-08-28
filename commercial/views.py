from django.shortcuts import render
from django.http import *
from django.utils import http
from django.contrib import auth
from django.contrib.auth.models import User
from datetime import *
from django.views.decorators.csrf import csrf_exempt
from django.template.loader import get_template
from django.template import Context
from django.views.generic import  TemplateView
from .models import *
from baby.models import *
from users.utils import *
from utils.serialization import *
import hashlib, time, random, json
# Create your views here.


def web_view(request):
    try:
        if request.method != 'GET':
            return HttpResponse(json_serialize(status = 'HTTP_METHOD_ERR'))
        if not request.GET.get('id'):
            return HttpResponseNotFound(json_serialize(status = 'NOT_FOUND'))
        cid = request.GET.get('id')
        if cid == None or cid =="":
            return HttpResponseNotFound(json_serialize(status = 'NOT_FOUND'))
        cid = int(cid)
        try:
            o = Commercial.objects.get(id = cid)
        except Commercial.DoesNotExist:
            return HttpResponseNotFound(json_serialize(status = 'NOT_FOUND'))
        t = get_template('commercial/commercial.html')
        c = {}
        c['commercial_commercialid'] = o.id
        c['commercial_title'] = o.title
        c['commercial_content'] = o.content
        c['commercial_address'] = o.merchant.address
        c['commercial_url'] = "www.yangwabao.com"
        picindex = random.randint(0,9)
        c['pic'] = o.photo.url
        c['comments'] = CommercialComment.objects.filter(commercialid=o)
        c['comments_size'] = len(c['comments'])
        html = t.render(Context(c))
        return HttpResponse(html)
    except ValueError:
        raise Http404()

def mobile_web_view(request, commercialid):
    try:
        cid = int(commercialid)
        try:                                                                                   
            o = Commercial.objects.get(id = cid)                             
        except Commercial.DoesNotExist:                                                        
            return HttpResponseNotFound(json_serialize(status = 'NOT_FOUND'))                  
        t = get_template('commercial/commercial.html')                                         
        c = {}                                                                                 
        c['commercial_commercialid'] = o.id                                                    
        c['commercial_title'] = o.title                                                        
        c['commercial_content'] = o.content                                                    
        c['commercial_address'] = o.merchant.address                                           
        #c['commercial_url'] = "www.yangwabao.com"
        c['commercial_phonenumber'] = o.merchant.phonenumber
        c['commercial_fromdate'] = o.valid_date_from
        c['commercial_enddate'] = o.valid_date_end
        c['merchant_id'] = o.merchant.id
        picindex = random.randint(0,9)                                                         
        c['pic'] = o.photo.url
        c['comments'] = CommercialComment.objects.filter(commercialid=o)                       
        c['comments_size'] = len(c['comments'])                                                
        html = t.render(Context(c))                                                            
        return HttpResponse(html)
    except ValueError:
        raise Http404()


def list_commercial(request):
    try:
        if request.method != 'GET':
            return HttpResponse(json_serialize(status = 'HTTP_METHOD_ERR'))
        cnumber = int(request.GET.get('number'))
        if  cnumber == None:
            cnumber = 2
        else:
            cnumber = int(cnumber)
        (authed, username, password, user) = auth_user(request)
        if not authed or not user:
            print("##not authed in commercial")
            commercials = getcommerciallist_anonymous(request, cnumber)
            #return HttpResponse(json.dumps(commercials, ensure_ascii=False))
            return HttpResponse(json_serialize(status='OK',result=commercials))
        else:
            try:
                baby = Baby.objects.get(user=user)
                commercials = getcommerciallist(baby, cnumber)
                #return HttpResponse(json.dumps(commercials, ensure_ascii=False))
                return HttpResponse(json_serialize(status='OK',result=commercials))
            except Baby.DoesNotExist:
                return HttpResponse(json_serialize(status = 'BABY_NULL'))
    except Exception as e:
        print('Exception:' + str(e))
        return HttpResponse(json_serialize(status = 'EXCEPTION', result = str(e)))


@csrf_exempt
def addcomment(request, commercialid):
    try:
        if request.method != 'POST':
            return HttpResponse(json_serialize(status = 'HTTP_METHOD_ERR'))
        (authed, username, password, user) = auth_user(request)
        if not authed or not user:
            return HttpResponse(json_serialize(status = 'AUTH_FAILED'))
        commercial = Commercial.objects.get(id=int(commercialid))
        timenow = datetime.datetime.utcnow().replace(tzinfo=utc)
        
        commercialcomment = CommercialComment(commercialid=commercial, comment=request.POST['commercialcomment'], from_user=user, create_time=timenow)
        commercialcomment.save()
        #return web_view(request)
        return mobile_web_view(request, commercialid)
    except Exception as e:
        print('Exception:' + str(e))
        return HttpResponse(json_serialize(status = 'EXCEPTION', result = str(e)))
