from django.test import TestCase
from django.utils import timezone
from django.contrib.auth.models import User
from kaeru.models import Project
from kaeru.models import Code
from kaeru.models import Page

class LoginTest(TestCase):

    def setUp(self):
        User(
            username="anon",
            first_name="anon",
            last_name="anon",
            email="anon@anon.anon",
            password="a2e6fff81614f079077573df38ad10a1",
         ).save()

    def test_login_nouser(self):
        response = self.client.post('/login/', {})
        self.assertEqual(200, response.status_code)

    def test_login_nopass(self):
        response = self.client.post('/login/', {'username': 'ben'})
        self.assertEqual(200, response.status_code)

    def test_login_invalid_username(self):
        username = ""
        password = ""
        response = self.client.post('/login/', {'username': username,
                                                'password': password})
        self.assertEqual(200, response.status_code)

    def test_login_invalid_password(self):
        username = User.objects.get().username
        password = "invalid"
        response = self.client.post('/login/', {'username': username,
                                                'password': password})
        self.assertEqual(200, response.status_code)

    def test_login_success(self):
        user = User.objects.get()
        response = self.client.post('/login/', {'username': user.username,
                                                'password': user.password})
        self.assertEqual(200, response.status_code)


# class UserDataTest(TestCase):
#     def test_





# AboutTest ?
class UrlsTest(TestCase):

    def test_login_page_exists(self):
        """
        Check that there is a login page
        """
        response = self.client.get('/login/')
        self.assertEqual(200, response.status_code)

    def test_index_exists(self):
        """
        Check that index (landing) page exists
        """
        response = self.client.get('/')
        self.assertEqual(200, response.status_code)

    def test_documentation_exists(self):
        """
        Check that documentation page exists
        """
        response = self.client.get('/documentation/')
        self.assertEqual(200, response.status_code)

    def test_people_exists(self):
        """
        Check that people page exists
        """
        response = self.client.get('/people/')
        self.assertEqual(200,response.status_code)

    def test_projects_exists(self):
        """
        Check that projects page exists
        """
        response = self.client.get('/projects/')
        self.assertEqual(302,response.status_code) # 302? 200?

    def test_change_password_exists(self):
        """
        Check that change_password page exists
        """
        response = self.client.get('/change_password/')  # 302? 200?
        self.assertEqual(302,response.status_code)

    def test_404(self):
        """
        Raise an arbitrary 404
        """
        pagename = "arbitraryname"
        response = self.client.get('/%s/' % pagename)
        self.assertEqual(404, response.status_code)

# Testing adding projects as a user
class ProjectTest(TestCase):

    # Pre-test setup of a user
    def setUp(self):
        User(
            username="anon",
            first_name="anon",
            last_name="anon",
            email="anon@anon.anon",
            password="a2e6fff81614f079077573df38ad10a1",
         ).save()

    # Tests user creation and deletion of projects using the view
    # 1-creation of project in default view
    # 2-creation of project in user view
    # 3-deletion of project
    def test_create_project_view(self):

        # Initial account setup and signing
        response = self.client.post('/signup/', {'username': 'dummyName',
                                                'password': 'dummyPass',
                                                'email': 'dummy@email.com',
                                                'first_name': 'Dummy',
                                                'last_name': 'Name'})
        self.assertEqual(200, response.status_code)

        user = User.objects.get(username='dummyName')

        response = self.client.post('/login/', {'username': 'dummyName',
                                                'password': 'dummyPass'})
        self.assertEqual(200, response.status_code)

        # Creating a project through default view
        response = self.client.post('/projects/', {'operation': 'add',
                                                   'projectname': 'MyFirstProject'})
        self.assertEqual(200, response.status_code)

        # Check if project has been added to database
        project = Project.objects.all().filter(creator=user)[0]
        self.assertEqual("MyFirstProject",project.name)

        # Creating a project through general account view
        response = self.client.post('/projects/dummyName/', {'operation': 'add',
                                                             'projectname': 'MySecondProject'})
        self.assertEqual(200, response.status_code)

        # Check if project has been added to database
        project = Project.objects.all().filter(creator=user)[1]
        self.assertEqual("MySecondProject",project.name)

        # Deleting a project
        response = self.client.post('/projects/dummyName/', {'operation': 'delete',
                                                            'projectname': 'MyFirstProject'})
        self.assertEqual(200, response.status_code)

        # Check if project has been deleted from database
        project = Project.objects.all().filter(creator=user)[0]
        self.assertEqual("MySecondProject",project.name);

    # Test user creation of projects
    def test_create_project(self):

        user = User.objects.get(username="anon")

        # Creating a project under anon
        Project(
            name="MyFirstProject", 
            creator=user,
            create_date=timezone.now()
         ).save()

        # Check if project has been added to database
        project = Project.objects.all().filter(creator=user)[0]
        self.assertEqual("MyFirstProject",project.name);

    # Test listing contributors of projects
    def test_project_contributors(self):

        user = User.objects.get(username="anon")

        # Creating a project under anon and adding anon as a contributor
        p = Project(
            name="MyFirstProject", 
            creator=user,
            create_date=timezone.now()
         )
        p.save()
        p.contributors.add(user)
        p.save()

        # Check if anon is a contributor
        project = Project.objects.all().filter(creator=user)[0]
        self.assertEqual("anon",project.contributors.all()[0].username);

	#This function tests:
	#1-creation of code object
	#2-assignment of a project to it
    def test_project_to_codes(self):
        n = Code(
            filePathAndName = "filename",
            created = timezone.now()
        )
        n.save()
        p = Project(
            name="MyFirstProject", 
            creator=User.objects.get(username="anon"),
            create_date=timezone.now()
        )
        p.save()
        n.projects.add(p)
        n.save()
        self.assertEqual(n.projects.all()[0].name,"MyFirstProject");

    #This function tests:
	#1-creation of code object
	#2-assignment of a code object to project object
    def test_codes_to_project(self):
        n2 = Code(
            filePathAndName = "filename",
            created = timezone.now()
        )
        n2.save()
        p2 = Project(
            name="MyFirstProject", 
            creator=User.objects.get(username="anon"),
            create_date=timezone.now()
        )
        p2.save()
        p2.codes.add(n2)
        p2.save()
        self.assertEqual(n2.projects.all()[0].name,"MyFirstProject");

    def test_projectcode_to_page(self):
        p = Project(
            name="MyFirstProject",
            creator=User.objects.get(username="anon"),
            create_date=timezone.now()
        )
        p.save()
        c = Code(
            filePathAndName="filename",
            created=timezone.now()

        )
        c.save()
        page = Page(
            page_name="pagename",
            page_create_date=timezone.now(),
            page_modify_date=timezone.now(),
        )
        page.save()
        page.project=p
        page.code_set.add(c)
        page.save()
        self.assertEqual(page.project.name,"MyFirstProject")
        self.assertEqual(page.code_set.all()[0].filePathAndName,"filename")

    def test_page_to_project(self):
        p = Project(
            name="MyFirstProject",
            creator=User.objects.get(username="anon"),
            create_date=timezone.now()
        )
        p.save()
        page = Page(
            page_name="pagename",
            page_create_date=timezone.now(),
            page_modify_date=timezone.now(),
        )
        page.save()
        p.page_set.add(page)
        p.save()
        self.assertEqual(p.page_set.all()[0].page_name,"pagename")

    def test_page_to_code(self):
        c = Code(
            filePathAndName="filename",
            created=timezone.now()

        )
        c.save()
        page = Page(
            page_name="pagename",
            page_create_date=timezone.now(),
            page_modify_date=timezone.now(),
        )
        page.save()
        c.page=page
        c.save()
        self.assertEqual(c.page.page_name,"pagename")