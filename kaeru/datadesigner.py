__author__ = 'lingbokou'


from django.template.loader import get_template
from django.template import Template,Context
from django.http import HttpResponse
import json
from collections import namedtuple

#Test the form generated from json string
def test(request):
    options=['test1','test2']
    t=get_template('datadesigner.html')
    context={}
    context['options']=options
    json1='{"tablename":"student","fields": [{"name":"id","type":"integer","allownull":"on"},{"name":"friends","type":"list","second":"student"}]}'
    x = json.loads(json1, object_hook=lambda d: namedtuple('X', d.keys())(*d.values()))
    context['jsonin']=x
    html=t.render(Context(context))
    return HttpResponse(html)





