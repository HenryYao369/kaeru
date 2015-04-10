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

    def test_about_exists(self):
        """
        Check that each about page exists
        """
        from kaeru.views import ABOUT_PAGES
        for pagename in ABOUT_PAGES:
            response = self.client.get('/about/%s/' % pagename)
            self.assertEqual(200, response.status_code)

    def test_about_404(self):
        """
        Raise an arbitrary 404 in the views.about function
        """
        from kaeru.views import ABOUT_PAGES
        pagename = "".join(ABOUT_PAGES)
        response = self.client.get('/about/%s/' % pagename)
        self.assertEqual(404, response.status_code)

    def test_about_default(self):
        """
        Check that default about page exists
        """
        response = self.client.get('/about/')
        self.assertEqual(200, response.status_code)

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