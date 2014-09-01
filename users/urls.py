'''
Created on Nov 2, 2013

@author: shengeng
'''
from django.conf.urls import patterns, url

from users import views

urlpatterns = patterns('',
    url(r'^register/', views.register, name='register'),
    url(r'^update/', views.update, name='update'),
    url(r'^login/', views.user_login, name='user_login'),
    url(r'^logout/', views.user_logout, name='user_logout'),
    url(r'^info/', views.getinfo, name='getinfo'),
    url(r'^posthead/', views.upload_head, name='posthead'),
    url(r'^gethead/', views.get_head, name='gethead'),
    
#     url(r'^informationcheck/', views.informationcheck, name='informationcheck'),
    url(r'^gethomepic/', views.gethomepic, name='gethomepic'),
)