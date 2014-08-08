from django.conf import settings
from django.contrib.auth import authenticate
from django.http import Http404
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.core.context_processors import csrf

import os

# These pages should live in 'kaeru/templates/about/'
# Alternatively, these names could live in a database
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
    cookie = {}
    cookie.update(csrf(request)) # Required for csrf form protection
    if request.method == "POST":
        # Try to log the user in, else show the 'create account' page
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)
        user = authenticate(username=username, password=password)
        if user is None:
            cookie['error_message'] = "Login failed."
        elif not (user.is_active):
            cookie['error_message'] = "Username/Password combo is valid, but the account has been disabled."
        else:
            # User is valid, active, and authenticated
            cookie['error_message'] = None
            cookie['user'] = user
        return render_to_response('login.html', cookie)
    else:
        # Show the login page
        return render_to_response('login.html', cookie)

