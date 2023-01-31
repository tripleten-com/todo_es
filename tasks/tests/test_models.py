# tasks/tests/tests_models.py
from django.test import TestCase

from tasks.models import Task


class TaskModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Create a test record in the database and
        # save it as a class variable
        # We do not specify the slug value, we expect that when creating
        # it will be created automatically from the title.
        # And we will make the title so that after transliteration it becomes
        # more than 100 characters
        #
        cls.task = Task.objects.create(
            title='I am a str'*10,
            text='Test body'
        )
        # print(len(cls.task.title))

    def test_verbose_name(self):
        """verbose_name of the fields matches the expected values."""
        task = TaskModelTest.task
        field_verboses = {
            'title': 'Заголовок',
            'text': 'Текст',
            'slug': 'Адрес для страницы с задачей',
            'image': 'Картинка',
        }
        for value, expected in field_verboses.items():
            with self.subTest(value=value):
                self.assertEqual(
                    task._meta.get_field(value).verbose_name, expected)

    def test_help_text(self):
        """help_text of the fields matches the expected values."""
        task = TaskModelTest.task
        field_help_texts = {
            'title': 'Enter task name',
            'text': 'Enter task description',
            'slug': ('Enter a unique URL for the task page. Use only '
                     'Latin characters, numbers, hyphens, and underscores'),
            'image': 'Upload an image',
        }
        for value, expected in field_help_texts.items():
            with self.subTest(value=value):
                self.assertEqual(
                    task._meta.get_field(value).help_text, expected)

    def test_text_convert_to_slug(self):
        """The value of title is converted into slug."""
        task = TaskModelTest.task
        slug = task.slug
        self.assertEquals(slug, 'i-am-a-str'*10)

    def test_text_slug_max_length_not_exceed(self):
        """
        A longer slug is truncated to avoid exceeding the slug model field max_length.
        """
        task = TaskModelTest.task
        max_length_slug = task._meta.get_field('slug').max_length
        length_slug = len(task.slug)
        self.assertEqual(max_length_slug, length_slug)

    def test_object_name_is_title_fild(self):
        """The __str__ field of the task object contains the value of the task.title field."""
        task = TaskModelTest.task
        expected_object_name = task.title
        self.assertEqual(expected_object_name, str(task))
