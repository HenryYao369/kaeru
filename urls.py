from django.conf.urls.defaults import *
from django.conf import settings
from settings import ISPRODUCTION

# Uncomment the next two lines to enable the admin:
#from django.contrib import admin
#admin.autodiscover()

if ISPRODUCTION:
    urlpatterns = patterns('',
                           (r'^kaeru-lang.org/', include('kaeru.urls')),
                           )
else:
    urlpatterns = patterns('',
                           (r'^', include('kaeru.urls')),
                           )

if settings.DEBUG:
    # this needs to be at the top level for the students when 
    # running on their laptops. ???
    urlpatterns += patterns('',
                            (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.TOPDIR + '/static/'}),
    )
