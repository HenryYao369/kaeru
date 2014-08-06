from django.test import TestCase

class UrlsTest(TestCase):
    def test_index_exists(self):
        """
        Check that index (landing) page exists
        """
        response = self.client.get('/')
        self.assertEqual(200, response.status_code)

    def test_about_pages_exist(self):
        """
        Check that each about page exists
        """
        from kaeru.views import ABOUT_PAGES
        for pagename in ABOUT_PAGES:
            response = self.client.get('/about/%s/' % pagename)
            self.assertEqual(200, response.status_code)

    def test_about_page_404(self):
        """
        Raise an arbitrary 404 in the views.about function
        """
        from kaeru.views import ABOUT_PAGES
        pagename = "".join(ABOUT_PAGES)
        response = self.client.get('/about/%s/' % pagename)
        self.assertEqual(404, response.status_code)

    def test_about_page_default(self):
        """
        Check that default about page exists
        """
        response = self.client.get('/about/')
        self.assertEqual(200, response.status_code)

    def test_login_page_exists(self):
        """
        Check that there is a login page
        """
        response = self.client.get('/login/')
        self.assertEqual(200, response.status_code)
