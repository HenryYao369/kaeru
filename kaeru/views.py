from django.conf import settings
from django.http import Http404
from django.http import HttpResponse
from django.shortcuts import render_to_response
import os

# These pages should live in 'kaeru/templates/about/'
ABOUT_PAGES = [
    'about',
    'documentation',
    'download',
    'faq',
    'news',
    'people',
    'publications',
    'support',
    'tutorial',
]
def about(request, pagename='about'):
    # Search for a matching template page, raise 404 if none found.
    if pagename in ABOUT_PAGES:
        return render_to_response('about/%s.html' % pagename, {})
    else:
        raise Http404

def index(request):
    return render_to_response('index.html', {})

def login(request):
    if request.method == "POST":
        # Try to log the user in, else show the 'create account' page
        return render_to_response('login.html', {})
    else:
        # Show the login page
        return render_to_response('login.html', {})
