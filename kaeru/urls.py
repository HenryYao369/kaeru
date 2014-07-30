from django.conf.urls.defaults import *
from django.conf import settings


# django docs here 'https://docs.djangoproject.com/en/1.4/topics/http/urls/'
urlpatterns = patterns('kaeru.views',
    # LHS is the url pattern, RHS is a function pointer. Regex groups are passed as args to the function pointer
    (r'^$', 'main'),
    (r'^about/(?P<page>.*)/$', 'about'),
    # (r'^dispatch/(?P<sourcename>[a-z]+)/(?P<methodname>[a-z]+)/((?P<arg1>[a-zA-Z0-9\-]+)/)?$', 'dispatch'),
)

if settings.DEBUG:
    # this needs to be in vnotary for the debugged production environment
    urlpatterns += patterns('',
                            (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.TOPDIR + '/static/'}),
    )

