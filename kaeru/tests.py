from django.test import TestCase
from django.utils import timezone
from django.contrib.auth.models import User

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
