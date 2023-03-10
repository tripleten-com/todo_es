from django.contrib.auth import get_user_model
from django.test import TestCase, Client

from tasks.models import Task

User = get_user_model()


class TaskURLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        # Crea un registro en la base de datos para comprobar la disponibilidad de task/test-slug/
        Task.objects.create(
            title='Título de prueba',
            text='Cuerpo de prueba',
            slug='test-slug',
        )

    def setUp(self):
        # Crea un cliente no autorizado
        self.guest_client = Client()
        # Crea un cliente autorizado
        self.user = User.objects.create_user(username='NoraStrong')
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    # Probar las páginas disponibles para todos los usuarios
    def test_home_url_exists_at_desired_location(self):
        """La página / está disponible para todos los usuarios."""
        response = self.guest_client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_task_added_url_exists_at_desired_location(self):
        """La página /added/ está disponible para todos los usuarios."""
        response = self.guest_client.get('/added/')
        self.assertEqual(response.status_code, 200)

    # Comprueba la disponibilidad de las páginas para los usuarios autorizados
    def test_task_list_url_exists_at_desired_location(self):
        """La página /task/ está disponible para los usuarios autorizados."""
        response = self.authorized_client.get('/task/')
        self.assertEqual(response.status_code, 200)

    def test_task_detail_url_exists_at_desired_location_authorized(self):
        """La página /task/test-slug/ está disponible para los usuarios autorizados."""
        response = self.authorized_client.get('/task/test-slug/')
        self.assertEqual(response.status_code, 200)

    # Comprueba si hay usuarios no autorizados en las redirecciones
    def test_task_list_url_redirect_anonymous_on_admin_login(self):
        """La página /task/ redirige a usuarios no 
        autorizados a la página de inicio.
        """
        response = self.guest_client.get('/task/', follow=True)
        self.assertRedirects(
            response, '/admin/login/?next=/task/')

    def test_task_detail_url_redirect_anonymous_on_admin_login(self):
        """La página /task/test_slug/ redirecciona a usuarios no 
        autorizados a la página de inicio.
        """
        response = self.client.get('/task/test-slug/', follow=True)
        self.assertRedirects(
            response, ('/admin/login/?next=/task/test-slug/'))

    # Comprueba las plantillas de cada ruta
    def test_urls_uses_correct_template(self):
        """URL utiliza la plantilla correspondiente."""
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
