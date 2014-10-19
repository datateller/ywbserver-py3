'''
Created on Nov 2, 2013

@author: shengeng
'''
from django.conf.urls import patterns, url

from .views import *

urlpatterns = patterns('',
    url(r'^login/', login_view),
    url(r'^logout/', logout_view),
    url(r'^$', MerchantMainPageView.as_view(), name='merchant_mainpage'),
    url(r'^register/', RegisterView.as_view(success_url='/merchant/'), name='register'),
    url(r'^password_change/$', 'django.contrib.auth.views.password_change', {'template_name':'merchant/password_change.html'},name='password_change'),
    #url(r'^password_change/done/$', 'django.contrib.auth.views.password_change_done', name='password_change_done'),
    url(r'^password_change/done/$', MerchantHomeView.as_view(), name='password_change_done'),
    url(r'^password_reset/$', 'django.contrib.auth.views.password_reset', {'template_name':'merchant/password_reset_form.html', 'email_template_name':'merchant/password_reset_email.html'}, name='password_reset'),
    url(r'^password_reset/done/$', 'django.contrib.auth.views.password_reset_done', {'template_name':'merchant/password_reset_done.html'}, name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        'django.contrib.auth.views.password_reset_confirm', {'template_name':'merchant/password_reset_confirm.html'},
        name='password_reset_confirm'),
    url(r'^reset/done/$', 'django.contrib.auth.views.password_reset_complete', {'template_name':'merchant/password_reset_complete.html'}, name='password_reset_complete'),
    url(r'^home/', MerchantHomeView.as_view(), name='merchant_home'),
    #url(r'^commercials/promotioneffect/(\d+)/', PromotionView.as_view(), name='promotion_effect'),
    url(r'^commercials/post/', CommercialPostView.as_view(success_url='/merchant/commercials/list/'), name='commercials_post'),
    url(r'^commercials/list/', CommercialListView.as_view(), name='commercials_list'),
    url(r'^commercials/promotion/', CommercialPromotionView.as_view(), name='commercials_promotion'),
    url(r'^commercials/promotioneffect/(?P<commercial_id>\d+)/', PromotionView.as_view(), name='promotion_effect'),
    url(r'^commercials/userresponses/(?P<commercial_id>\d+)/', CommercialReceiptView.as_view(), name='commercial_receipt'),
    url(r'^commercials/comments/(?P<commercial_id>\d+)/', CommercialCommentView.as_view(), name='commercial_comment'),
    url(r'^commercials/commentresponse/(?P<commercial_id>\d+)/(?P<comment_id>\d+)/',commercial_comment_response_view),
    url(r'^commercials/', CommercialListView.as_view(), name='commercials'),
    url(r'^about$', about, name='about'),
    url(r'^findhelp/', FindHelpView.as_view(), name='findhelp'),
    url(r'^comments/', MerchantCommentsView.as_view(), name='merchant_comments'),
    url(r'^resp_user_demand/', resp_user_demand_view),
    url(r'^publish_findhelp/', publish_findhelp),
    url(r'^getsurr/', surrounding_view),
    url(r'^user_demand_related_merchant/', user_demand_related_merchant_view),
    url(r'^merchantdetail/(?P<merchant_id>\d+)/', MerchantDetailView.as_view(), name='merchant detail'),
    url(r'^mobile_single_userdemand/', mobile_single_userdemand, name='single userdemand'),
)

