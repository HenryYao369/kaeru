from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
# admin.autodiscover() # 2014-07-30: raises 500's when uncommented

urlpatterns = patterns('',
    url(r'^admin/'  , include(admin.site.urls)), # enables django admin
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')), #enables django admin docs

    url(r'^$'       , 'kaeru.views.index'),
    url(r'^login/$' , 'kaeru.views.login'), 
    url(r'^logout/$' , 'kaeru.views.logout'), 
    url(r'^secret/$' , 'kaeru.views.secret'), 
    url(r'^signup/$' , 'kaeru.views.signup'),
    url(r'^about/$' , 'kaeru.views.about'),
    url(r'^about/(?P<pagename>[a-z\-]+)/$', 'kaeru.views.about'),
)
