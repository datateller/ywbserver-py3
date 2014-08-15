from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib import auth
from django.http import *
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_GET
from django.core.paginator import Paginator, EmptyPage
from tlquan.models import TlTopic
from jiaquan.models import JiaTopic
from merchant.models import UserDemand, userdemandslist_encode
from utils.serialization import *
from users.utils import *

# Create your views here.

def get_page_and_number(request):
     page = request.GET.get('page')
     if not page:
         page = 1
     else:
         page = int(page)

     number = request.GET.get('number')
     if not number:
         number = 5
     else:
         number = int(number)

     return page, number

@login_required
@require_GET
def list_person_topics(request):
    try:
        (authed, username, password, user) = auth_user(request)
        if not authed or not user:
            return HttpResponse("AUTH_FAILED")
        tltopics = TlTopic.objects.filter(from_user=request.user)
        jiaquantopics = JiaTopic.objects.filter(from_user=request.user)
    
        page, number = get_page_and_number(request)

        topics_list = list(tltopics)+list(jiaquantopics)
        topics_list.sort(key=lambda topic:topic.update_time, reverse=True)
        paginator = Paginator(topics_list, number)
        try:
            return HttpResponse(json_serialize(status='OK', result={'topics':circletopiclist_encode(paginator.page(page))}))
        except EmptyPage:
            return HttpResponse(json_serialize(status='OK', result={'topics':circletopiclist_encode(paginator.page(paginator.num_pages))}))
    except Exception as e:
        import traceback
        traceback.print_stack()
        print("####exception:",e)
        return HttpResponse(json_serialize(status='EXCEPTION'))

   
@login_required
@require_GET
def list_person_userdemand(request):
    try:   
        (authed, username, password, user) = auth_user(request)
        if not authed or not user:                                                             
            return HttpResponse("AUTH_FAILED")
 
        page, number = get_page_and_number(request)       
       
        mydemands = UserDemand.objects.filter(user=request.user) 
        mydemands_list = list(mydemands)
        mydemands_list.sort(key=lambda demand:demand.pub_time, reverse=True)
        paginator = Paginator(mydemands_list, number)
        try:
            return HttpResponse(json_serialize(status='OK', result={'userdemands':userdemandslist_encode(paginator.page(page))}))
        except EmptyPage:
            return HttpResponse(json_serialize(status='OK', result={'userdemands':userdemandslist_encode(paginator.page(paginator.num_pages))}))

    except Exception as e:
        print("##exception",e)
        return HttpResponse(json_serialize(status='EXCEPTION'))
      
