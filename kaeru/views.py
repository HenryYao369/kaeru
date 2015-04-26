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
from kaeru.models import Project
from django.utils import timezone
from django.db.models import Q

from django.utils import timezone
from kaeru.models import Code

import os

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

@login_required
def projects_view(request, urlusername=None, urlprojectname=None):

    # Get information
    cookie = _get_csrf_cookie(request)
    username = request.user.username # Username info
    isuser = (urlusername is None) or (username == urlusername) # Whether or not user is responsible for this view

    # Specified user: display specified user's projects page
    if (urlusername is None) or (urlusername is not None and urlprojectname is None):

        if isuser:
            user = User.objects.get(username=username)
        else:
            user = User.objects.get(username=urlusername)

        # Handle POST requests
        if request.method == "POST":
            operation = request.POST.get('operation', None)
            projectname = request.POST.get('projectname', None)
            hidden = request.POST.get('hidden', False)
            if user is not None and projectname is not None and isuser:
                if operation == 'delete': # Delete the given project
                    Project.objects.all().filter(creator=user).filter(name=projectname).delete()
                elif operation == 'add': # Add a new project
                    p = Project(
                        name=projectname, 
                        creator=user,
                        hidden=hidden,
                        create_date=timezone.now()
                     )
                    p.save()
                    p.contributors.add(user)
                    p.save()

        # Display project listings
        if isuser: # Own projects
            cookie['username'] = username
            cookie['projects'] = Project.objects.all().filter(creator=user) # All created projects
        else: # Others' projects
            cookie['username'] = urlusername
            publiccriterion = Q(creator=user, hidden=False) # Want to show public projects
            contributorcriterion = Q(creator=user, hidden=True, contributors__username=username) # Also want to show contributed projects
            cookie['projects'] = Project.objects.all().filter(publiccriterion | contributorcriterion)
        cookie['isuser'] = isuser
        return render_to_response('projects.html', cookie)

    # Specified user and project: display specified project page
    elif urlusername is not None and urlprojectname is not None:
        # Handle POST requests
        if request.method == "POST":
            operation = request.POST.get('operation', None)
            contributorname = request.POST.get('contributorname', None)
            if isuser:
                if operation == 'addcontributor': # Add a contributor to a project
                    project = Project.objects.all().filter(name=urlprojectname)[0] # Specific project
                    contributor = User.objects.get(username=contributorname)
                    project.contributors.add(contributor)
                    project.save()
                elif operation == 'rmcontributor': # Remove a contributor from a project
                    project = Project.objects.all().filter(name=urlprojectname)[0] # Specific project
                    contributor = User.objects.get(username=contributorname)
                    project.contributors.remove(contributor)
                    project.save()

        # Display project information
        project = Project.objects.all().filter(name=urlprojectname) # Specific project
        cookie['username'] = urlusername
        cookie['projectname'] = urlprojectname
        cookie['iscreator'] = (urlusername == username) # Dictate delete permissions
        cookie['contributors'] = project[0].contributors.all() # TODO: Change so that we don't use zero-index
        return render_to_response('project.html', cookie)

    # Other: do nothing
    else:
        return None

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
