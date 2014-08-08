from django.conf import settings
from django.contrib import auth
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
def about_view(request, pagename='about'):
    # Search for a matching template page, raise 404 if none found.
    if pagename in ABOUT_PAGES:
        return render_to_response('about/%s.html' % pagename, {})
    else:
        raise Http404

def index_view(request):
    return render_to_response('index.html', {})

def _get_csrf_cookie(request):
    # Authenticate cookies for django csrf (cross-site reference) forms
    cookie = {}
    cookie.update(csrf(request)) # Required for csrf form protection
    return cookie

def login_view(request):
    # Log existing user into the system
    cookie = _get_csrf_cookie(request)
    if request.method == "POST":
        # Try to log the user in, else show the 'create account' page
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)
        user = auth.authenticate(username=username,password=password)
        if user is None:
            cookie['error_message'] = "Login failed."
        elif not (user.is_active):
            cookie['error_message'] = "Username/Password combo is valid, but the account has been disabled."
        else:
            # User is valid, active, and authenticated
            auth.login(request, user)
            cookie['username'] = user.username
            cookie['error_message'] = None
        return render_to_response('login.html', cookie)
    else:
        # Show the login page
        return render_to_response('login.html', cookie)

def logout_view(request):
    if request.user and request.user.is_authenticated:
        # Successful logout
        username = request.user.username
        auth.logout(request)
        return render_to_response('logout.html', {username: username})
    else:
        # Logout is a no-op. Nobody was logged in.
        return render_to_response('logout.html', {})

def secret_view(request):
    # testing. Only logged-in users can see this
    if not_auth:
        redirect_to_login('secret/')
    return 
    
def signup_view(request):
    cookie = _get_csrf_cookie(request)
    url = 'signup.html'
    if request.method == "POST":
        # Create the account
        user, is_new = auth.models.User.objects.get_or_create(
                   username   = request.POST.get('username', None),
                   email      = request.POST.get('email', None),
                   password   = request.POST.get('password', None),
                   first_name = request.POST.get('first_name', None),
                   last_name  = request.POST.get('last_name', None),
            )
        cookie['username'] = user.username
        if is_new:
            # Just made a new user. Welcome aboard!
            user.groups.add(auth.models.Group.objects.get(name="KaeruUsers"))
            return render_to_response(url, cookie)
        else:
            # Existing user. Welcome back!
            return render_to_response('login.html', cookie)
    else:
        # Show the sign up page
        return render_to_response(url, cookie)
