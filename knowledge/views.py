from django.shortcuts import render
from django.http import *
from baby.models import Baby
from knowledge.models import *
from django.contrib import auth
from django.contrib.auth.models import User
from django.utils import http
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import FormView, TemplateView, CreateView
from datetime import *
from users.utils import *
import base64, json, random, math

from django.template.loader import get_template
from django.template import Context
from .forms import *
from ywbserver.settings import *
# Create your views here.

def web_view(request):
    try:
        kid = request.GET.get('id')
        if kid == None or kid =="":
            return HttpResponseNotFound("Not Found")
        kid = int(kid)
        try:
            k = Knowledge.objects.get(id = kid)
        except Knowledge.DoesNotExist:
            return HttpResponseNotFound("Not Found")
        content = k.content
        html = content
        adaptorstr = '''<meta name="viewport" content="width=device-width,initial-scale=1,maximum-scale=1,minimum-scale=1" />'''
        imagestyle = '''<style type="text/css"> div img { display:none } </style>'''
        split1 = html.split('<head>')
        html = ('%s <head> %s %s %s') % (split1[0], adaptorstr, imagestyle, split1[1])

        imagestart = html.find('<img')
        if imagestart < 0:
           print("##no image")
           picindex = random.randint(0,9)
           imgstr = '''
<p style=\"text-align: center\">
  <img src=\"%s\" style=\"width: 300px; height: 241px, display:inline\"/>
</p>
''' % ('http://wjbb.cloudapp.net:8001/pic/'+str(picindex)+'.jpg')
           htmlsplit = html.split('<body>')
           html = ('%s <body> %s %s')%(htmlsplit[0], imgstr, htmlsplit[1])

        else:
            print("image")
            srcstart = html.find("src", imagestart)
            srcend = html.find("\"", srcstart + 5)
            imageurl = html[srcstart+5:srcend]
            imgstr = '''
<p style=\"text-align: center\">
  <img src=\"%s\" style=\"width: 300px; height: 241px, display:inline\"/>
</p>
''' % (imageurl)
            htmlsplit = html.split('<body>')
            html = ('%s <body> %s %s')%(htmlsplit[0], imgstr, htmlsplit[1])
        print(html)
        return HttpResponse(html)
    except ValueError:
        raise Http404()


class KnowledgeFormView(CreateView):
    template_name = 'knowledge/knowledgeform.html'
    form_class = KnowledgeForm
    model = Knowledge
    

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


def getknowllist(baby, number):
    if(baby and baby.birthday):
        age= (int((date.today() - baby.birthday).days))
        response = knowledge_list_encode(get_knowls_byage(age, number))
    else:
        response = knowledge_list_encode(get_knowls_random(number))
    return response


def getknowllist_anonymous(request, number):
    if not request.GET.get('age'):
        print("get knowlist randomly.")
        return knowledge_list_encode(get_knowls_random(number))
    age = int(request.GET.get('age'))
    print("get knowlist by age %d" % age)
    return knowledge_list_encode(get_knowls_byage(age, number))
     

def list_knowledge(request):
    try:
        if request.method != 'GET':
            return HttpResponse('HTTP_METHOD_ERR')
        knumber = 5
        if request.GET.get('number'):
            knumber = int(request.GET.get('number'))
        (authed, username, password, user) = auth_user(request)
        if not authed or not user:
            knowls = getknowllist_anonymous(request, knumber)
            return HttpResponse(json.dumps(knowls, ensure_ascii=False))
        else:
            baby = Baby.objects.get(user=user)
            knowls = getknowllist(baby, knumber)
            return HttpResponse(json.dumps(knowls, ensure_ascii=False))
    except Exception as e:
        print('Exception:' + str(e))
        return HttpResponse('EXCEPTION')


@csrf_exempt
def collectknowl(request):
    try:
        if request.method == 'GET':
                return HttpResponse('HTTP_METHOD_ERR')
        (authed, username, password, user) = auth_user(request)
        if not authed or not user:
            return HttpResponse('AUTH_FAILED')
        knowlid = request.POST.get('id')
        if knowlid == None or knowlid =="":
            return HttpResponse('NULL_ID')
        else:
            knowlid = int(knowlid)
        try:
            collection_record = KnowledgeCollection.objects.get(user = user)
        except KnowledgeCollection.DoesNotExist:
            new_collection_record = KnowledgeCollection(user = user, collections = [])
            new_collection_record.collections.append(knowlid)
            new_collection_record.save()
            return HttpResponse('OK')
        else:
            if knowlid not in collection_record.collections:
                collection_record.collections.append(knowlid)
                collection_record.save()
            return HttpResponse('OK')
    except Exception as e:
        print('Exception:' + str(e))
        return HttpResponse('EXCEPTION')


def list_collection(request):
    try:
        if request.method != 'GET':
            return HttpResponse('HTTP_METHOD_ERR')
        (authed, username, password, user) = auth_user(request)
        if not authed or not user:
            return HttpResponse('AUTH_FAILED')
        knumber = request.GET.get('number')
        if knumber == None:
            knumber = 5
        else:
            knumber = int(knumber)
        collection = user.knowledgecollection
        if not collection:
            return HttpResponse(json.dumps({}, ensure_ascii=False))
        knowlids = collection.collections
        knowls = get_knowls_byids(knowlids)
        return HttpResponse(json.dumps(knowledge_list_encode(knowls), ensure_ascii=False))
    except Exception as e:
        print('Exception:' + str(e))
        return HttpResponse('EXCEPTION')
