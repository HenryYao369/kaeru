from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
# admin.autodiscover() # 2014-07-30: raises 500's when uncommented

urlpatterns = patterns('',
    url(r'^admin/'  , include(admin.site.urls)), # enables django admin
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')), #enables django admin docs

    url(r'^$'       , 'kaeru.views.index_view'),
    #url(r'^about/$' , 'kaeru.views.about_view'),
    #url(r'^about/(?P<pagename>[a-z\-]+)/$', 'kaeru.views.about_view'),
    url(r'^documentation/$' , 'kaeru.views.documentation_view'), 
    url(r'^login/$' , 'kaeru.views.login_view'), 
    url(r'^logout/$' , 'kaeru.views.logout_view'),
    url(r'^signup/$' , 'kaeru.views.signup_view'),
    url(r'^people/$' , 'kaeru.views.people_view'),
    url(r'^ide/$' , 'kaeru.views.ide_view')
)
