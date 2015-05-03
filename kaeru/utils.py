from django.utils import timezone
from django.contrib.auth.models import User
from kaeru.models import Project
from kaeru.models import Page
from kaeru.models import Code

# Handles a post request made from a user-projects management view
# Operations:
#   add - add project
#   rm - remove project
# Additional arguments:
#   user - user object
#   project_name - name of the project
#   hidden - whether or not project is hidden
def handle_user_post(operation, **kwargs):
    try:
        if operation == 'add': # Add a new project
            project = Project(
                name=kwargs['project_name'], 
                creator=kwargs['user'],
                hidden=kwargs['hidden'],
                create_date=timezone.now()
             )
            project.save()
            # project.contributors.add(kwargs['user'])
            # project.save()
        elif operation == 'rm': # Delete the given project and all associated pieces
            project = Project.objects.get(creator=kwargs['user'], name=kwargs['project_name']) # Specific project
            pages = Page.objects.all().filter(project=project)
            for page in pages:
                Code.objects.get(page=page).delete()
                page.delete()
            project.delete()
    except (User.DoesNotExist, Project.DoesNotExist, Page.DoesNotExist, Code.DoesNotExist):
        pass

# Handles a post request made from a single project management view
# Operations:
#   add_contributor - add a contributor to the project
#   rm_contributor - remove a contributor from the project
#   add_page - add a page to this project
#   rm_page - remove a page from this project
#   publicize - make project public
#   privatize - make project private
# Additional arguments:
#   creator - user object representing the creator of the project
#   project_name - name of the project
#   contributor_name - name of the relevant contributor
#   page_name - name of the relevant page
def handle_project_post(operation, **kwargs):
    try:
        # Obtain project information
        project = Project.objects.get(creator=kwargs['creator'], name=kwargs['project_name'])

        if operation == 'add_contributor': # Add a contributor to a project
            contributor = User.objects.get(username=kwargs['contributor_name'])
            project.contributors.add(contributor)
            project.save()
        elif operation == 'rm_contributor': # Remove a contributor from a project
            contributor = User.objects.get(username=kwargs['contributor_name'])
            project.contributors.remove(contributor)
            project.save()
        elif operation == 'add_page': # Add a page and default code to a project
            page = Page(
                page_name=kwargs['page_name'],
                project=project
             )
            page.save()
            code = Code(
                page=page
             )
            code.save()
        elif operation == 'rm_page': # Remove a page from a project and all associated pieces
            page = Page.objects.all().filter(page_name=kwargs['page_name'],project=project)
            Code.objects.all().filter(page=page).delete()
            page.delete()
        elif operation == 'publicize': # Add a contributor to a project
            project.hidden = False;
            project.save()
        elif operation == 'privatize': # Remove a contributor from a project
            project.hidden = True;
    except (User.DoesNotExist, Project.DoesNotExist, Page.DoesNotExist, Code.DoesNotExist):
        pass

# Handles a post request made from a page management view
# Operations:
#   modify_code - modifies the code backing this page
# Additional arguments:
#   creator - user object representing the creator of the project
#   project_name - name of the project
#   page_name - name of the page
#   code - code for the page
def handle_page_post(operation, **kwargs):
    try:
        # Obtain page information
        project = Project.objects.get(creator=kwargs['creator'], name=kwargs['project_name'])
        page = Page.objects.get(page_name=kwargs['page_name'],project=project)

        if operation == 'modify_code': # Add a contributor to a project
            code = Code.objects.get(page=page)
            code.code = kwargs['code']
            code.save()
    except (User.DoesNotExist, Project.DoesNotExist, Page.DoesNotExist, Code.DoesNotExist):
        pass