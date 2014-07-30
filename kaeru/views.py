from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render_to_response

def index(request):
    return render_to_response('index.html', {'index': True})

def login(request):
    if request.method == "POST":
        # Try to log the user in, else show the 'create account' page
        return render_to_response('login.html', {})
    else:
        # Show the login page
        return render_to_response('login.html', {})
