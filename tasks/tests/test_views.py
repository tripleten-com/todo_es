from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse
from django import forms

from tasks.models import Task

User = get_user_model()


class TaskPagesTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        Task.objects.create(
            title='Title',
            text='Body',
            slug='test-slug',
        )

    def setUp(self):
        # Crea un cliente no autorizado
        self.guest_client = Client()
        # Crea un cliente autorizado
        self.user = User.objects.create_user(username='StasBasov')
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    # Prueba las plantillas llamadas
    def test_pages_uses_correct_template(self):
        """URL utiliza la plantilla correspondiente."""
        # Crea un diccionario de pares "html_template_name: reverse(name)".
        templates_page_names = {
            'tasks/home.html': reverse('tasks:home'),
            'tasks/added.html': reverse('tasks:task_added'),
            'tasks/task_list.html': reverse('tasks:task_list'),
            'tasks/task_detail.html': (
                reverse('tasks:task_detail', kwargs={'slug': 'test-slug'})
            ),
        }
        # Valida este nombre llamando
        # a la plantilla HTML correspondiente
        for template, reverse_name in templates_page_names.items():
            with self.subTest(template=template):
                response = self.authorized_client.get(reverse_name)
                self.assertTemplateUsed(response, template)

    def test_home_page_show_correct_context(self):
        """Los datos de contexto de la plantilla de inicio son correctos."""
        response = self.guest_client.get(reverse('tasks:home'))
        # Diccionario con los tipos de campo previstos:
        # especifica las clases apropiadas para los objetos de los campos de formulario
        form_fields = {
            'título': forms.fields.CharField,
            # Al crear un campo model de tipo TextField,
            # se convierte en CharField con el widget forms.Textarea
            'texto': forms.fields.CharField,
            'slug': forms.fields.SlugField,
            'imagen': forms.fields.ImageField,
        }

        # Comprueba que todos los tipos de campo del diccionario de contexto
        # son los previstos
        for value, expected in form_fields.items():
            with self.subTest(value=value):
                form_field = response.context['form'].fields[value]
                # Comprueba que el campo del formulario es una
                # instancia de la clase especificada
                self.assertIsInstance(form_field, expected)

    def test_task_list_page_list_is_1(self):
        # Make sure that the page with the list of tasks is passed
        # expected number of objects
        
        response = self.authorized_client.get(reverse('tasks:task_list'))
        self.assertEqual(response.context['object_list'].count(), 1)

    # Comprueba que el diccionario contextual de la página /task
    # contiene los valores previstos en el primer elemento de object_list
    def test_task_list_page_show_correct_context(self):
        """Los datos de contexto de la plantilla task_list son correctos."""
        response = self.authorized_client.get(reverse('tasks:task_list'))
        # Toma el primer elemento de la lista y comprueba que su valor
        # coincide con el previsto
        first_object = response.context['object_list'][0]
        task_title_0 = first_object.title
        task_text_0 = first_object.text
        task_slug_0 = first_object.slug
        self.assertEqual(task_title_0, 'Título')
        self.assertEqual(task_text_0, 'Cuerpo')
        self.assertEqual(task_slug_0, 'test-slug')

    # Comprueba que el diccionario contextual de la página task/test-slug
    # coincide con el previsto
    def test_task_detail_pages_show_correct_context(self):
        """Los datos de contexto de la plantilla task_detail son correctos."""
        response = self.authorized_client.get(
            reverse('tasks:task_detail', kwargs={'slug': 'test-slug'})
            )
        self.assertEqual(response.context['task'].title, 'Título')
        self.assertEqual(response.context['task'].text, 'Cuerpo')
        self.assertEqual(response.context['task'].slug, 'test-slug')

    def test_initial_value(self):
        """Valor de forma actual."""
        response = self.guest_client.get(reverse('tasks:home'))
        title_inital = response.context['form'].fields['title'].initial
        self.assertEqual(title_inital, 'Valor por defecto')
