from django.contrib.auth import get_user_model
from django.test import TestCase, Client

from tasks.models import Task

User = get_user_model()


class TaskURLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        # Create a database record to check the availability of task/test-slug/
        Task.objects.create(
            title='Test title',
            text='Test body',
            slug='test-slug',
        )

    def setUp(self):
        # Create an unauthorized client
        self.guest_client = Client()
        # Create an authorized client
        self.user = User.objects.create_user(username='StasBasov')
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    # Test the pages available to all users
    def test_home_url_exists_at_desired_location(self):
        """Page / is available to all users."""
        response = self.guest_client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_task_added_url_exists_at_desired_location(self):
        """Page /added/ is available to all users."""
        response = self.guest_client.get('/added/')
        self.assertEqual(response.status_code, 200)

    # Check the availability of pages to authorized users
    def test_task_list_url_exists_at_desired_location(self):
        """Page /task/ is available to authorized users."""
        response = self.authorized_client.get('/task/')
        self.assertEqual(response.status_code, 200)

    def test_task_detail_url_exists_at_desired_location_authorized(self):
        """Page /task/test-slug/ is available to authorized users."""
        response = self.authorized_client.get('/task/test-slug/')
        self.assertEqual(response.status_code, 200)

    # Check the redirects for unauthorized users
    def test_task_list_url_redirect_anonymous_on_admin_login(self):
        """Page /task/ redirects unauthorized
        users to the login page.
        """
        response = self.guest_client.get('/task/', follow=True)
        self.assertRedirects(
            response, '/admin/login/?next=/task/')

    def test_task_detail_url_redirect_anonymous_on_admin_login(self):
        """Page /task/test_slug/ redirects unauthorized
        users to the login page.
        """
        response = self.client.get('/task/test-slug/', follow=True)
        self.assertRedirects(
            response, ('/admin/login/?next=/task/test-slug/'))

    # Check the templates for each path
    def test_urls_uses_correct_template(self):
        """URL uses the corresponding template."""
        templates_url_names = {
            'tasks/home.html': '/',
            'tasks/added.html': '/added/',
            'tasks/task_list.html': '/task/',
            'tasks/task_detail.html': '/task/test-slug/',
        }
        for template, url in templates_url_names.items():
            with self.subTest(url=url):
                response = self.authorized_client.get(url)
                self.assertTemplateUsed(response, template)
