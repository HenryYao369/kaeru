from django.test import TestCase
from django.utils import timezone
from kaeru.models import User


class LoginTest(TestCase):

    def setUp(self):
        User(name="anon",
             favorite_color="anon",
             email="anon@anon.anon",
             create_date=timezone.now(),
             login_date=timezone.now()
         ).save()

    def test_login_nouser(self):
        response = self.client.post('/login/', {})
        self.assertEqual(200, response.status_code)
        # KLUDGE
        self.assertContains(response, "Please enter your username.")

    def test_login_nopass(self):
        response = self.client.post('/login/', {'username': 'ben'})
        self.assertContains(response, "Please enter your password.")

    def test_login_invalid_username(self):
        username = ""
        password = ""
        response = self.client.post('/login/', {'username': username,
                                                'password': password})
        self.assertContains(response, "not found.")

    def test_login_invalid_password(self):
        username = User.objects.get().name
        password = ""
        response = self.client.post('/login/', {'username': username,
                                                'password': password})
        self.assertContains(response, "Invalid password")

    def test_login_success(self):
        user = User.objects.get()
        response = self.client.post('/login/', {'username': user.name,
                                                'password': user.favorite_color})
        self.assertContains(response, "Welcome")


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
