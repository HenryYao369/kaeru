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
    url(r'^pages/(?P<url_username>([A-Za-z])\w+)/(?P<url_projectname>([A-Za-z])\w+)/(?P<url_pagename>([A-Za-z])\w+)/$' , 'kaeru.views.pages_view'), 
    url(r'^people/$' , 'kaeru.views.people_view'),



    url(r'^ide/$' , 'kaeru.views.ide_view'),

    url(r'^projects/$' , 'kaeru.views.projects_view'), 

    # url(r'^tutorial/$' , 'kaeru.views.tutorial_view'),    # comment out this line to enable admin site.

    url(r'^projects/(?P<url_username>([A-Za-z])\w+)/$' , 'kaeru.views.projects_view'), 
    url(r'^projects/(?P<url_username>([A-Za-z])\w+)/(?P<url_projectname>([A-Za-z])\w+)/$' , 'kaeru.views.projects_view'), 
    url(r'^projects/(?P<url_username>([A-Za-z])\w+)/(?P<url_projectname>([A-Za-z])\w+)/(?P<url_pagename>([A-Za-z])\w+)/$' , 'kaeru.views.projects_view'),

	url(r'^codes/$' , 'kaeru.views.codes_view'), 

	url(r'^codes_submit/$' , 'kaeru.views.codes_submit_view'), 

    url(r'^change_password/$', 'kaeru.views.change_password'),
    url(r'^change_password_ok/$', 'kaeru.views.change_password_ok'),

    url(r'^change_user_data/$', 'kaeru.views.change_user_data'),
    url(r'^change_user_data_ok/$', 'kaeru.views.change_user_data_ok'),



	url(r'^codes_submit/$' , 'kaeru.views.codes_submit_view'),
    url(r'datadesigner/$' , 'kaeru.datadesigner.test'),

)
