from django.contrib.auth.models import Group as DjangoGroup
from django.contrib.auth.models import User as DjangoUser
from django.conf import settings
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.core.context_processors import csrf
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models import Q

from django.utils import timezone
from kaeru.models import Project
from kaeru.models import Page
from kaeru.models import Code

import os
import kaeru.utils

# These pages should live in 'kaeru/templates/about/'
# Alternatively, these names could live in a database
#ABOUT_PAGES = [
#    'about',
#    'faq',
#    'people',
#    'support',
#]
#def about_view(request, pagename='about'):
#    # Search for a matching template page, raise 404 if none found.
#    if pagename in ABOUT_PAGES:
#        return render_to_response('about/%s.html' % pagename, {})
#    else:
#        raise Http404

def documentation_view(request):
    return render_to_response('documentation.html', {})

#def index_view(request):
#    return render_to_response('index.html', {})

def people_view(request):
    return render_to_response('people.html', {})

@login_required
def codes_view(request):
    cookie = _get_csrf_cookie(request)
    return render_to_response('codes.html', cookie)

@login_required
def codes_submit_view(request):

    cookie = _get_csrf_cookie(request)

    #
    filename = request.POST.get('filename', '')
    code = request.POST.get('code', '')
    
    #get username
    username = 'cem'
    
    filename = username + '-' + filename
    
    #assumes user gives a normal filename
    file = open(filename, 'w')
    file.write(code)
    file.close()

    Code(
        filePathAndName = filename,
        created = timezone.now()
    ).save()

    html = "<html>...Successfully created "+filename+"...</html>"
    return HttpResponse(html)

def _get_csrf_cookie(request):
    # Authenticate cookies for django csrf (cross-site reference) forms
    cookie = {}
    cookie.update(csrf(request)) # Required for csrf form protection
    if hasattr(request, 'user'):
        cookie['user'] = request.user
    return cookie

def login_view(request):
    # Log existing user into the system
    cookie = _get_csrf_cookie(request)
    if request.method == "POST":
        # Try to log the user in.
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)
        user = auth.authenticate(username=username,password=password)
        if user is None:
            cookie['error_message'] = "Login failed."
        elif not (user.is_active):
            cookie['error_message'] = "Username/Password combo is valid, but the account has been disabled."
        else:
            # User is valid, active, and authenticated. Log in.
            auth.login(request, user)
        return render_to_response('login.html', cookie)
    else:
        # Show the login page.
        return render_to_response('login.html', cookie)

def logout_view(request):
    if request.user.is_authenticated:
        # Successful logout
        username = request.user.username
        auth.logout(request)
        return render_to_response('logout.html', {'username': username})
    else:
        # Logout is a no-op. Nobody was logged in.
        return render_to_response('logout.html', {})

#@login_required
#def secret_view(request):
#    return render_to_response('secret.html', {})
    
#this used to be 'signup_view' and there used to be a separate 'index_view'
def index_view(request):
    cookie = _get_csrf_cookie(request)
    url = 'index.html'
    if request.method == "POST":
        # Create the account
        raw_username = request.POST.get('username', None)
        raw_password = request.POST.get('password', None)
        user, is_new = auth.models.User.objects.get_or_create(
                   username   = raw_username,
                   email      = request.POST.get('email', None),
                   first_name = request.POST.get('first_name', None),
                   last_name  = request.POST.get('last_name', None),
            )
        if is_new:
            # Just made a new user. Welcome aboard!
            user.set_password(raw_password)
            user.groups.add(auth.models.Group.objects.get(name="KaeruUsers"))
            user.save()
            cookie['signup_success'] = True
            cookie['user'] = user
            # log in
            auth.login(request, auth.authenticate(username=raw_username, password=raw_password))
            return render_to_response(url, cookie)
        else:
            # Existing user.
            cookie['duplicate_username'] = True
            return render_to_response(url, cookie)
    else:
        # Show the sign up page
        return render_to_response(url, cookie)

def signup_view(request):
    cookie = _get_csrf_cookie(request)
    url = 'signup.html'
    if request.method == "POST":
        # Create the account
        raw_username = request.POST.get('username', None)
        raw_password = request.POST.get('password', None)
        new_user, is_new = auth.models.User.objects.get_or_create(
                   username   = raw_username,
                   email      = request.POST.get('email', None),
                   first_name = request.POST.get('first_name', None),
                   last_name  = request.POST.get('last_name', None),
            )

        if is_new:
            # Just made a new user. Welcome aboard!
            new_user.set_password(raw_password)

            # user.groups.add(auth.models.Group.objects.get(name="KaeruUsers"))

            '''To create new Group. '''
            my_group, is_created = DjangoGroup.objects.get_or_create(name='KaeruUsers')
            new_user.groups.add(my_group)
            # mygroup.save()


            '''future work: set group permissions'''
            # my_group.permissions = [permission_list]


            new_user.save()
            cookie['signup_success'] = True
            cookie['user'] = new_user

            # log in
            auth.login(request, auth.authenticate(username=raw_username, password=raw_password))
            return render_to_response(url, cookie)

        else:
            # Existing user.
            cookie['duplicate_username'] = True
            return render_to_response(url, cookie)
    else:
        # Show the sign up page
        return render_to_response(url, cookie)

# The projects view is for user-based administrative management.
# Specifically, it allows them to do the following: 
#   - View their projects, pages, and code
#   - Create projects, pages for projects, and code for projects
#   - Update/Modify their projects, pages, and code
@login_required
def projects_view(request, url_username=None, url_projectname=None, url_pagename=None):

    # Get information
    cookie = _get_csrf_cookie(request)
    username = request.user.username # Username info
    is_user = (url_username is None) or (username == url_username) # Whether or not user is responsible for this view

    # Specified user: display specified user's projects page
    if url_projectname is None:

        try:
            if is_user:
                user = User.objects.get(username=username)
            else:
                user = User.objects.get(username=url_username)
    
            # Handle POST requests
            if request.method == "POST":
                if is_user:
                    kaeru.utils.handle_user_post(
                        request.POST.get('operation', None), 
                        user=user, 
                        project_name=request.POST.get('projectname', None), 
                        hidden=request.POST.get('hidden', False))
    
            # Display project listings
            if is_user: # Display all projects if user owns this account
                cookie['username'] = username
                cookie['projects'] = Project.objects.all().filter(creator=user) # All created projects
                cookie['contributions'] = Project.objects.all().filter(contributors__username=username) # All contributions
            else: # Otherwise, only display the projects that are public or the logged in user is contributing to
                cookie['username'] = url_username
    
                public_criterion = Q(creator=user, hidden=False) # Want to show public projects
                contributor_criterion = Q(creator=user, hidden=True, contributors__username=username) # Also want to show ones contributed to
                cookie['projects'] = Project.objects.all().filter(public_criterion | contributor_criterion)
    
                # public_criterion = Q(hidden=False, contributors__username=url_username) # Want to show public contributions
                # contributor_criterion = Q(hidden=True, contributors__username=url_username, contributors__username=username) # Also want to show mutual contributions
                # cookie['contributions'] = Project.objects.all().filter(public_criterion | contributor_criterion)
    
            cookie['isuser'] = is_user
            return render_to_response('projects.html', cookie)
        except User.DoesNotExist:
            return render_to_response('404.html')

    # Specified user and project: display specified project page
    elif url_pagename is None:
        try:
            creator = User.objects.get(username=url_username)
            # Check if contributor
            user = User.objects.get(username=username)
            project = Project.objects.get(creator=creator,name=url_projectname)
            is_contributor = is_user or (not project.hidden) or (user in project.contributors.all())
            if not is_contributor:
                return render_to_response('private.html')

            # Handle POST requests
            if request.method == "POST":
                if is_contributor:
                    kaeru.utils.handle_project_post(
                        request.POST.get('operation', None), 
                        creator=creator, 
                        project_name=url_projectname, 
                        contributor_name=request.POST.get('contributorname', None),
                        page_name=request.POST.get('pagename', None))

            # Display project information if valid
            project = Project.objects.get(creator=creator,name=url_projectname)
            cookie['username'] = url_username
            cookie['projectname'] = url_projectname
            cookie['iscreator'] = is_user # Dictate delete permissions
            cookie['iscontributor'] = is_contributor # Dictate delete permissions
            cookie['contributors'] = project.contributors.all()
            cookie['pages'] = Page.objects.all().filter(project=project)
            return render_to_response('project.html', cookie)
        except (User.DoesNotExist, Project.DoesNotExist):
            return render_to_response('404.html')

    # Specified user, project, and page: display specified page
    else:
        try:
            creator = User.objects.get(username=url_username)
            # Check if contributor
            user = User.objects.get(username=username)
            project = Project.objects.get(creator=creator,name=url_projectname)
            is_contributor = is_user or (not project.hidden) or (user in project.contributors.all())
            if not is_contributor:
                return render_to_response('private.html')

            # Handle POST requests
            if request.method == "POST":
                if is_contributor:
                    kaeru.utils.handle_page_post(
                        request.POST.get('operation', None), 
                        creator=creator, 
                        project_name=url_projectname,
                        page_name=url_pagename,
                        code=request.POST.get('code', None))

            # Display project information if valid
            project = Project.objects.get(creator=creator,name=url_projectname)
            page = Page.objects.get(project=project,page_name=url_pagename)
            code = Code.objects.get(page=page)
            cookie['username'] = url_username
            cookie['projectname'] = url_projectname
            cookie['pagename'] = page.page_name
            cookie['code'] = code.code
            return render_to_response('pages.html', cookie)
        except (Project.DoesNotExist, Page.DoesNotExist, Code.DoesNotExist):
            return render_to_response('404.html')

# The pages view is for public viewing of served pages
def pages_view(request, url_username=None, url_projectname=None, url_pagename=None):

    if url_username is None or url_projectname is None or url_pagename is None:
        return render_to_response('404.html')

    # Obtain the relevant JScript code associated with the page
    try:
        creator = User.objects.get(username=url_username)
        project = Project.objects.get(creator=creator,name=url_projectname)
        page = Page.objects.get(project=project,page_name=url_pagename)
        code = Code.objects.get(page=page)
        # Load the HTML template with the relevant JScript code
        cookie = {
            'code': code.code
            }
        return render_to_response('page.html', cookie)
    except (User.DoesNotExist, Project.DoesNotExist, Page.DoesNotExist, Code.DoesNotExist):
        return render_to_response('404.html')