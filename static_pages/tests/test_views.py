from django.test import Client, TestCase
from django.urls import reverse


class StaticViewsTests(TestCase):
    def setUp(self):
        self.guest_client = Client()

    def test_about_page_accessible_by_name(self):
        """URL generada con el nombre static_pages: about, available."""
        response = self.guest_client.get(reverse('static_pages:about'))
        self.assertEqual(response.status_code, 200)

    def test_about_page_uses_correct_template(self):
        """Al enviar un staticpages:about
        se aplica la plantilla staticpages/about.html."""
        response = self.guest_client.get(reverse('static_pages:about'))
        self.assertTemplateUsed(response, 'static_pages/about.html')
