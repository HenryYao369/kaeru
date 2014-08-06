from django.conf import settings
from django.http import Http404
from django.http import HttpResponse
from django.shortcuts import render_to_response

from kaeru.models import User

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
    if request.method == "POST":
        # Try to log the user in, else show the 'create account' page
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)
        # Error fallback
        if username is None:
            errormsg = "Please enter your username."
        elif password is None:
            errormsg = "Please enter your password."
        elif not User.objects.filter(name=username):
            errormsg = "Username '%s' not found." % username
        elif not User.objects.filter(name=username, favorite_color=password):
            # TODO replace with passwordhash
            errormsg = "Invalid password"
        else:
            # Find user, TODO save user to session.
            # TODO httpresponseredirect
            errormsg = None
            user = User.objects.filter(name=username,favorite_color=password)[0]
            return render_to_response('login.html', {"user": user})
        return render_to_response('login.html', {"error_message": errormsg})
    else:
        # Show the login page
        return render_to_response('login.html', {})

