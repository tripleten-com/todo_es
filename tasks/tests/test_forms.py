import shutil
import tempfile

from tasks.forms import TaskCreateForm
from tasks.models import Task
from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client, TestCase, override_settings
from django.urls import reverse

# Create a temporary folder for media files
# We'll override the media folder for the test
TEMP_MEDIA_ROOT = tempfile.mkdtemp(dir=settings.BASE_DIR)


# We'll use the temporary folder TEMP_MEDIA_ROOT
# for saving media files during the test, and then we'll delete it
@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class TaskCreateFormTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Create a database record to validate the existing slug
        Task.objects.create(
            title='Test title',
            text='Test body',
            slug='first'
        )
        # Create a form if you need to validate the attributes
        cls.form = TaskCreateForm()

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        # shutil is a Python library with useful tools
        # for managing files and directories, including 
        # creating, deleting, copying, moving, and editing
        # The shutil.rmtree method deletes the directory and all its content
        shutil.rmtree(TEMP_MEDIA_ROOT, ignore_errors=True)

    def setUp(self):
        # Create an unauthorized client
        self.guest_client = Client()

    def test_create_task(self):
        """Valid form creates a record in Task."""
        # Count the number of records in Task
        tasks_count = Task.objects.count()
        # To test image upload,
        small_gif = (
            b'\x47\x49\x46\x38\x39\x61\x01\x00'
            b'\x01\x00\x00\x00\x00\x21\xf9\x04'
            b'\x01\x0a\x00\x01\x00\x2c\x00\x00'
            b'\x00\x00\x01\x00\x01\x00\x00\x02'
            b'\x02\x4c\x01\x00\x3b'
        )
        uploaded = SimpleUploadedFile(
            name='small.gif',
            content=small_gif,
            content_type='image/gif'
        )
        form_data = {
            'title': 'Test title',
            'text': 'Test body',
            'image': uploaded,
        }
        response = self.guest_client.post(
            reverse('tasks:home'),
            data=form_data,
            follow=True
        )
        # Test if the redirect works
        self.assertRedirects(response, reverse('tasks:task_added'))
        # Check if the number of posts increased
        self.assertEqual(Task.objects.count(), tasks_count+1)
        # Check that the record with the specified slug has been created
        self.assertTrue(
            Task.objects.filter(
                slug='testovyij-zagolovok',
                text='Test body',
                image='tasks/small.gif'
                ).exists()
        )

    def test_cant_create_existing_slug(self):
        # Count the number of records in Task
        tasks_count = Task.objects.count()
        form_data = {
            'title': 'Title from the form',
            'text': 'Body from the form',
            'slug': 'first',  # Try to submit a slug already existing in the database
        }
        # Send a POST request
        response = self.guest_client.post(
            reverse('tasks:home'),
            data=form_data,
            follow=True
        )
        # Make sure that the database record was not created
        # Compare the number of records in Task before and after submitting the form
        self.assertEqual(Task.objects.count(), tasks_count)
        # Check that the form returned an appropriate error:
        # take the 'form' dictionary from the response object
        # and specify the expected error for the 'slug' field of this dictionary
        self.assertFormError(
            response,
            'form',
            'slug',
            'Slug "first" already exists, enter a unique slug'
        )
        # Check that the site didn't crash and that the page returns a 200 status code
        self.assertEqual(response.status_code, 200)

    # If you haven't tested the contents of labels in models
    # or redefined them when creating the form - we test like this:
    def test_title_label(self):
        title_label = TaskCreateFormTests.form.fields['title'].label
        self.assertEqual(title_label, 'Title')

    def test_title_help_text(self):
        title_help_text = TaskCreateFormTests.form.fields['title'].help_text
        self.assertEqual(title_help_text, 'Enter task name')
