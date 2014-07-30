from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
# admin.autodiscover() # 2014-07-30: raises 500's when uncommented

urlpatterns = patterns('',
    # Enables the admin
    url(r'^admin/', include(admin.site.urls)),
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # url(r'^$', include('kaeru.urls')),
    url(r'^$', 'kaeru.views.index'),
)
