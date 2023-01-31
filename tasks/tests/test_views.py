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
        # Create an unauthorized client
        self.guest_client = Client()
        # Create an authorized client
        self.user = User.objects.create_user(username='StasBasov')
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    # Test the called templates
    def test_pages_uses_correct_template(self):
        """URL uses the corresponding template."""
        # Create a dictionary of "html_template_name: reverse(name)" pairs
        templates_page_names = {
            'tasks/home.html': reverse('tasks:home'),
            'tasks/added.html': reverse('tasks:task_added'),
            'tasks/task_list.html': reverse('tasks:task_list'),
            'tasks/task_detail.html': (
                reverse('tasks:task_detail', kwargs={'slug': 'test-slug'})
            ),
        }
        # Validate that name calls
        # the corresponding HTML template
        for template, reverse_name in templates_page_names.items():
            with self.subTest(template=template):
                response = self.authorized_client.get(reverse_name)
                self.assertTemplateUsed(response, template)

    def test_home_page_show_correct_context(self):
        """Context data of the template home is correct."""
        response = self.guest_client.get(reverse('tasks:home'))
        # Dictionary with the expected field types:
        # specify the appropriate classes for the form fields objects
        form_fields = {
            'title': forms.fields.CharField,
            # When you create a model field of type TextField,
            # it's converted to CharField with the widget forms.Textarea
            'text': forms.fields.CharField,
            'slug': forms.fields.SlugField,
            'image': forms.fields.ImageField,
        }

        # Test that all field types in the context dictionary
        # are as expected
        for value, expected in form_fields.items():
            with self.subTest(value=value):
                form_field = response.context['form'].fields[value]
                # Test that the form field is an
                # instance of the specified class
                self.assertIsInstance(form_field, expected)

    def test_task_list_page_list_is_1(self):
        # Make sure that the page with the list of tasks is passed
        # expected number of objects
        
        response = self.authorized_client.get(reverse('tasks:task_list'))
        self.assertEqual(response.context['object_list'].count(), 1)

    # Test that the context dictionary of the page /task
    # contains the expected values in the first element of object_list
    def test_task_list_page_show_correct_context(self):
        """Context data of the template task_list is correct."""
        response = self.authorized_client.get(reverse('tasks:task_list'))
        # Take the first list element and check that its value
        # matches the expected
        first_object = response.context['object_list'][0]
        task_title_0 = first_object.title
        task_text_0 = first_object.text
        task_slug_0 = first_object.slug
        self.assertEqual(task_title_0, 'Title')
        self.assertEqual(task_text_0, 'Body')
        self.assertEqual(task_slug_0, 'test-slug')

    # Check that the context dictionary of the page task/test-slug
    # matches the expected
    def test_task_detail_pages_show_correct_context(self):
        """Context data of the template task_detail is correct."""
        response = self.authorized_client.get(
            reverse('tasks:task_detail', kwargs={'slug': 'test-slug'})
            )
        self.assertEqual(response.context['task'].title, 'Title')
        self.assertEqual(response.context['task'].text, 'Body')
        self.assertEqual(response.context['task'].slug, 'test-slug')

    def test_initial_value(self):
        """Preset form value."""
        response = self.guest_client.get(reverse('tasks:home'))
        title_inital = response.context['form'].fields['title'].initial
        self.assertEqual(title_inital, 'Default value')
