from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'ywbserver.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    #url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'apphome.views.index', name='index'),
    url(r'^index$', 'apphome.views.index', name='index'),
    url(r'^apphome/', include('apphome.urls')),
    url(r'^user/', include('users.urls')),
    url(r'^knowledge/', include('knowledge.urls')),
    #url(r'^appmerchant/', include('merchant.urls')),
    url(r'^appcommercial/', include('commercial.urls')),
    url(r'^merchant/', include('merchant.urls')),
    url(r'^merchant/accounts/', include('registration.backends.default.urls')),
    url(r'^jiaquan/', include('jiaquan.urls')),
    url(r'^tlquan/', include('tlquan.urls')),
    url(r'^photos/', include('photos.urls')),
    url(r'^weather/', include('weather.urls')),
    url(r'^weixin/', include('weixin.urls')),
    url(r'^personality/', include('personality.urls')),
    url(r'^rss/', include('rss.urls')),
    (r'^media/(?P<path>.*)$', 'django.views.static.serve', { 'document_root': settings.MEDIA_ROOT})
    
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
