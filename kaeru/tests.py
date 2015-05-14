from django.test import TestCase
from django.utils import timezone
from django.contrib.auth.models import User
from kaeru.models import Project
from kaeru.models import Code
from kaeru.models import Page
from django.test import Client, LiveServerTestCase
from django.contrib.auth.hashers import make_password


class AdminTest(LiveServerTestCase):
    def test_login(self):
        c = Client()

        response = c.get('/admin/')
        self.assertEquals(response.status_code,302)
        # self.assertTrue('Log in' in response.content)

        c.login(username = 'username',password='password')
        response = c.get('/admin/')
        self.assertEquals(response.status_code,302)
        # self.assertTrue('Log out' in response.content)

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

    def xx(self):
        '''
        there should be a admin site login test!
        :return:
        '''


class UserPasswordChangeTest(TestCase):

    def test_user_pwd1(self):
        c = Client()

        response = self.client.post('/signup/', {'username': 'username',
                                                'password': 'old_pwd',
                                                'email': 'old@email.com',
                                                'first_name': 'old_first_name2',
                                                'last_name': 'old_last_name'})
        self.assertEqual(200, response.status_code)

        c.login(username='username', password='old_pwd')

        response=c.post('/change_password/', {'oldpassword': 'old_pwd',
                                                   'newpassword': 'new_pwd',
                                                   'newpassword1': 'new_pwd'})
        self.assertEqual(302, response.status_code)

        user = User.objects.get(username='username')
        self.assertEqual(True,user.check_password("new_pwd"))


class UserDataTest(TestCase):

    def test_user_data1(self):
        c = Client()

        response = self.client.post('/signup/', {'username': 'username',
                                                'password': 'old_pwd',
                                                'email': 'old@email.com',
                                                'first_name': 'old_first_name2',
                                                'last_name': 'old_last_name'})
        self.assertEqual(200, response.status_code)

        c.login(username='username', password='old_pwd')

        response=c.post('/change_user_data/', {'new_first_name': 'newFN',
                                                   'new_last_name': 'newLN',
                                                   'new_email': 'new@email.com'})
        user = User.objects.get(username='username')
        self.assertEqual(302, response.status_code)

        self.assertEqual("newFN",user.first_name)
        self.assertEqual("newLN",user.last_name)
        self.assertEqual("new@email.com",user.email)


    def test_user_data(self):
        # Initial account setup and signing
        response = self.client.post('/signup/', {'username': 'username',
                                                'password': 'old_pwd',
                                                'email': 'old@email.com',
                                                'first_name': 'old_first_name',
                                                'last_name': 'old_last_name'})
        self.assertEqual(200, response.status_code)

        # user = User.objects.get(username='old_username')

        response = self.client.post('/login/', {'username': 'old_username',
                                                'password': 'old_pwd'})
        self.assertEqual(200, response.status_code)


        response = self.client.post('/change_user_data/', {'new_first_name': 'newFN',
                                                   'new_last_name': 'newLN',
                                                   'new_email': 'new@email.com'})
        self.assertEqual(302, response.status_code) # Since we use Redirect here, it is 302 not 200.


        response = self.client.get('/change_user_data_ok/')
        self.assertEqual(200, response.status_code)


        self.client.logout()
        self.client.login(username='username', password='old_pwd')

        user = User.objects.get(username='username')
        self.assertEqual("newFN",user.first_name)
        self.assertEqual("newLN",user.last_name)
        self.assertEqual("new@email.com",user.email)







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
        self.assertEqual(200,response.status_code)


    def test_ide_exists(self):
        """
        Check that IDE page exists
        """
        response = self.client.get('/ide/')
        self.assertEqual(200,response.status_code)


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

        # Test 1 - Creating a project through default view
        response = self.client.post('/projects/', {'operation': 'add',
                                                   'projectname': 'MyFirstProject'})
        self.assertEqual(200, response.status_code)
        project = Project.objects.get(creator=user)
        self.assertEqual("MyFirstProject",project.name)

        # Test 2 - Creating a project through general account view
        response = self.client.post('/projects/dummyName/', {'operation': 'add',
                                                             'projectname': 'MySecondProject'})
        self.assertEqual(200, response.status_code)
        project = Project.objects.all().filter(creator=user)[1]
        self.assertEqual("MySecondProject",project.name)

        # Test 3 - Deleting a project
        response = self.client.post('/projects/dummyName/', {'operation': 'rm',
                                                            'projectname': 'MyFirstProject'})
        self.assertEqual(200, response.status_code)
        project = Project.objects.get(creator=user)
        self.assertEqual("MySecondProject",project.name);

    # Tests user creation and deletion of project pages using the view
    # 1-creation of project in default view
    # 2-creation of page in project view
    # 3-addition of code to page
    # 4-removal of page in project view
    def test_create_pages_view(self):

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

        # Test 1 - Creating a project through default view
        response = self.client.post('/projects/', {'operation': 'add',
                                                   'projectname': 'MyFirstProject'})
        self.assertEqual(200, response.status_code)

        project = Project.objects.get(creator=user)
        self.assertEqual("MyFirstProject",project.name)

        # Test 2 - Creating a page through projects view
        response = self.client.post('/projects/dummyName/MyFirstProject/', 
            {'operation': 'add_page', 'pagename': 'MyFirstPage'})
        self.assertEqual(200, response.status_code)

        page = Page.objects.get(project=project)
        self.assertEqual("MyFirstPage",page.page_name)

        # Test 3 - Addition of code to page
        code = Code.objects.get(page=page)
        self.assertEqual("",code.code)

        # Test 4 - Deleting a page
        response = self.client.post('/projects/dummyName/MyFirstProject/', 
            {'operation': 'rm_page', 'pagename': 'MyFirstPage'})
        self.assertEqual(200, response.status_code)
        self.assertEqual(0,len(Page.objects.all()));

    # Tests user modification of code using the view
    # 1-creation of project in default view
    # 2-creation of page in project view
    # 3-modification of code in page view
    def test_create_code_view(self):

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

        # Test 1 - Creating a project through default view
        response = self.client.post('/projects/', {'operation': 'add',
                                                   'projectname': 'MyFirstProject'})
        self.assertEqual(200, response.status_code)
        project = Project.objects.get(creator=user)
        self.assertEqual("MyFirstProject",project.name)

        # Test 2 - Creating a page through project view
        response = self.client.post('/projects/dummyName/MyFirstProject/', 
            {'operation': 'add_page', 'pagename': 'MyFirstPage'})
        self.assertEqual(200, response.status_code)
        page = Page.objects.get(project=project)
        self.assertEqual("MyFirstPage",page.page_name)

        # Test 3 - Modify the code for the page
        message = "var x = 10"
        response = self.client.post('/projects/dummyName/MyFirstProject/MyFirstPage/', 
            {'operation': 'modify_code', 'code': message})
        self.assertEqual(200, response.status_code)

        # Check if code for page has been modified
        code = Code.objects.get(page=page)
        self.assertEqual(message,code.code)

        # Check if code appears on the public page
        response = self.client.get('/pages/dummyName/MyFirstProject/MyFirstPage/')
        self.assertContains(response, message)

        # Check if random code doesn't appear
        self.assertNotContains(response, "var y = 30")

    # Tests project visibility of code using the view
    # 1-creation of public project
    # 2-non contributors can see public projects
    # 3-changing to private project
    # 4-non contributors cannot see public projects
    # 5-adding contributors
    # 6-contributors can see projects
    # 7-owners can see projects listed on contributors view
    # 8-contributors can see projects listed on other contributors view
    # 9-removing contributors
    # 10-changing to public project
    # 11-users can see public projects listed contributors view
    def test_contributors_view(self):

        # Initial account setup and signing
        response = self.client.post('/signup/', {'username': 'dummyName',
                                                'password': 'dummyPass',
                                                'email': 'dummy@email.com',
                                                'first_name': 'Dummy',
                                                'last_name': 'Name'})
        self.assertEqual(200, response.status_code)
        response = self.client.post('/signup/', {'username': 'dummyName2',
                                                'password': 'dummyPass2',
                                                'email': 'dummy@email.com',
                                                'first_name': 'Dummy',
                                                'last_name': 'Name'})
        self.assertEqual(200, response.status_code)
        response = self.client.post('/signup/', {'username': 'dummyName3',
                                                'password': 'dummyPass3',
                                                'email': 'dummy@email.com',
                                                'first_name': 'Dummy',
                                                'last_name': 'Name'})
        self.assertEqual(200, response.status_code)

        user = User.objects.get(username='dummyName')
        user2 = User.objects.get(username='dummyName2')
        user3 = User.objects.get(username='dummyName3')
        projectName = "MyFirstProject"
        privateMsg = "You do not have permission to view this project."

        # Test 1 - creation of public project
        response = self.client.post('/login/', {'username': 'dummyName',
                                                'password': 'dummyPass'})
        response = self.client.post('/projects/', {'operation': 'add',
                                                   'projectname': projectName})
        self.assertEqual(200, response.status_code)
        project = Project.objects.get(creator=user,name=projectName);
        self.assertEqual(False, project.hidden);
        response = self.client.post('/logout/')

        # Test 2 - non contributors can see public projects
        response = self.client.post('/login/', {'username': 'dummyName2',
                                                'password': 'dummyPass2'})
        response = self.client.get('/projects/dummyName/')
        self.assertContains(response, projectName)
        response = self.client.post('/logout/')

        # Test 3 - changing to private project
        response = self.client.post('/login/', {'username': 'dummyName',
                                                'password': 'dummyPass'})
        response = self.client.post('/projects/dummyName/MyFirstProject/', {'operation': 'privatize',
                                                                  'projectname': projectName})
        self.assertEqual(200, response.status_code)
        project = Project.objects.get(creator=user,name=projectName);
        self.assertEqual(True, project.hidden);
        response = self.client.post('/logout/')

        # Test 4 - non contributors cannot see public projects
        response = self.client.post('/login/', {'username': 'dummyName2',
                                                'password': 'dummyPass2'})
        response = self.client.get('/projects/dummyName/')
        self.assertNotContains(response, "MyFirstProject")
        response = self.client.get('/projects/dummyName/MyFirstProject/')
        self.assertContains(response, privateMsg)
        response = self.client.post('/logout/')

        # 5-adding contributors
        response = self.client.post('/login/', {'username': 'dummyName',
                                                'password': 'dummyPass'})
        response = self.client.post('/projects/dummyName/MyFirstProject/', {'operation': 'add_contributor',
                                                                  'projectname': projectName,
                                                                  'contributorname': 'dummyName2'})
        self.assertEqual(200, response.status_code)
        project = Project.objects.get(creator=user,name=projectName);
        self.assertEqual(True, user2 in project.contributors.all());
        response = self.client.post('/projects/dummyName/MyFirstProject/', {'operation': 'add_contributor',
                                                                  'projectname': projectName,
                                                                  'contributorname': 'dummyName3'})
        self.assertEqual(200, response.status_code)
        project = Project.objects.get(creator=user,name=projectName);
        self.assertEqual(True, user3 in project.contributors.all());
        response = self.client.post('/logout/')

        # 6-contributors can see projects
        response = self.client.post('/login/', {'username': 'dummyName2',
                                                'password': 'dummyPass2'})
        response = self.client.get('/projects/dummyName/')
        self.assertContains(response, "MyFirstProject")
        response = self.client.get('/projects/dummyName/MyFirstProject/')
        self.assertNotContains(response, privateMsg)
        response = self.client.post('/logout/')

        # 7-owners can see projects listed on contributors view
        response = self.client.post('/login/', {'username': 'dummyName',
                                                'password': 'dummyPass'})
        response = self.client.get('/projects/dummyName2/')
        self.assertContains(response, "MyFirstProject")
        response = self.client.post('/logout/')

        # 8-contributors can see projects listed on other contributors view
        response = self.client.post('/login/', {'username': 'dummyName3',
                                                'password': 'dummyPass3'})
        response = self.client.get('/projects/dummyName2/')
        self.assertContains(response, "MyFirstProject")
        response = self.client.post('/logout/')

        # 9-removing contributors
        response = self.client.post('/login/', {'username': 'dummyName',
                                                'password': 'dummyPass'})
        response = self.client.post('/projects/dummyName/MyFirstProject/', {'operation': 'rm_contributor',
                                                                  'projectname': projectName,
                                                                  'contributorname': 'dummyName2'})
        self.assertEqual(200, response.status_code)
        project = Project.objects.get(creator=user,name=projectName);
        self.assertEqual(False, user2 in project.contributors.all());
        response = self.client.post('/logout/')

        # 10-changing to public project
        response = self.client.post('/login/', {'username': 'dummyName',
                                                'password': 'dummyPass'})
        response = self.client.post('/projects/dummyName/MyFirstProject/', {'operation': 'publicize',
                                                                  'projectname': projectName})
        self.assertEqual(200, response.status_code)
        project = Project.objects.get(creator=user,name=projectName);
        self.assertEqual(False, project.hidden);
        response = self.client.post('/logout/')

        # 11-users can see public projects listed contributors view
        response = self.client.post('/login/', {'username': 'dummyName2',
                                                'password': 'dummyPass2'})
        response = self.client.get('/projects/dummyName3/')
        self.assertContains(response, "MyFirstProject")
        response = self.client.post('/logout/')

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
 #    def test_project_to_codes(self):
 #        n = Code(
 #            filePathAndName = "filename",
 #            created = timezone.now()
 #        )
 #        n.save()
 #        p = Project(
 #            name="MyFirstProject", 
 #            creator=User.objects.get(username="anon"),
 #            create_date=timezone.now()
 #        )
 #        p.save()
 #        n.projects.add(p)
 #        n.save()
 #        self.assertEqual(n.projects.all()[0].name,"MyFirstProject");

 #    #This function tests:
	# #1-creation of code object
	# #2-assignment of a code object to project object
 #    def test_codes_to_project(self):
 #        n2 = Code(
 #            filePathAndName = "filename",
 #            created = timezone.now()
 #        )
 #        n2.save()
 #        p2 = Project(
 #            name="MyFirstProject", 
 #            creator=User.objects.get(username="anon"),
 #            create_date=timezone.now()
 #        )
 #        p2.save()
 #        p2.codes.add(n2)
 #        p2.save()
 #        self.assertEqual(n2.projects.all()[0].name,"MyFirstProject");

 #    def test_projectcode_to_page(self):
 #        p = Project(
 #            name="MyFirstProject",
 #            creator=User.objects.get(username="anon"),
 #            create_date=timezone.now()
 #        )
 #        p.save()
 #        c = Code(
 #            filePathAndName="filename",
 #            created=timezone.now()

 #        )
 #        c.save()
 #        page = Page(
 #            page_name="pagename",
 #            page_create_date=timezone.now(),
 #            page_modify_date=timezone.now(),
 #        )
 #        page.save()
 #        page.project=p
 #        page.code_set.add(c)
 #        page.save()
 #        self.assertEqual(page.project.name,"MyFirstProject")
 #        self.assertEqual(page.code_set.all()[0].filePathAndName,"filename")

 #    def test_page_to_project(self):
 #        p = Project(
 #            name="MyFirstProject",
 #            creator=User.objects.get(username="anon"),
 #            create_date=timezone.now()
 #        )
 #        p.save()
 #        page = Page(
 #            page_name="pagename",
 #            page_create_date=timezone.now(),
 #            page_modify_date=timezone.now(),
 #        )
 #        page.save()
 #        p.page_set.add(page)
 #        p.save()
 #        self.assertEqual(p.page_set.all()[0].page_name,"pagename")

 #    def test_page_to_code(self):
 #        c = Code(
 #            filePathAndName="filename",
 #            created=timezone.now()

 #        )
 #        c.save()
 #        page = Page(
 #            page_name="pagename",
 #            page_create_date=timezone.now(),
 #            page_modify_date=timezone.now(),
 #        )
 #        page.save()
 #        c.page=page
 #        c.save()
 #        self.assertEqual(c.page.page_name,"pagename")
