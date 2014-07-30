
def shortname(): 
    return "login"

def description():
    return "Log in to your account"

def input(request):
    return django.shortcuts.render_to_response('plugins/login.html', {})
