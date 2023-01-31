from django.test import Client, TestCase


class StaticURLTests(TestCase):
    def setUp(self):
        self.guest_client = Client()

    def test_about_url_exists_at_desired_location(self):
        """Test the availability of /page/about/."""
        response = self.guest_client.get('/page/about/')
        self.assertEqual(response.status_code, 200)

    def test_about_url_uses_correct_template(self):
        """Test the template for /page/about/."""
        response = self.guest_client.get('/page/about/')
        self.assertTemplateUsed(response, 'static_pages/about.html')
