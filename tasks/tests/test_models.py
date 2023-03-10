# tasks/tests/tests_models.py
from django.test import TestCase

from tasks.models import Task


class TaskModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Crear un registro en la base de datos de prueba
        # guárdalo como variable de clase
        # No especificamos el valor de slug, esperamos que al crear
        # se creará automáticamente a partir del título.
        # Y haremos el título para que después de la transliteración se convierta en
        # más de 100 caracteres
        #
        cls.task = Task.objects.create(
            title='I am a str'*10,
            text='Cuerpo de prueba'
        )
        # print(len(cls.task.title))

    def test_verbose_name(self):
        """verbose_name de los diferentes campos coinciden con los valores previstos."""
        task = TaskModelTest.task
        field_verboses = {
            'title': 'Título',
            'text': 'Texto',
            'slug': 'El slug de la URL para la página de la tarea',
            'image': 'Imagen',
        }
        for value, expected in field_verboses.items():
            with self.subTest(value=value):
                self.assertEqual(
                    task._meta.get_field(value).verbose_name, expected)

    def test_help_text(self):
        """help_text en los diferentes campos coinciden con los valores previstos."""
        task = TaskModelTest.task
        field_help_texts = {
            'título': 'Introduce el nombre de la tarea',
            'texto': 'Introduce la descripción de la tarea',
            'slug': ('Introduce una URL única para la página de la tarea. Utiliza solo '
                     'Caracteres latinos, números, guiones y guiones bajos'),
            'imagen': 'Sube una imagen',
        }
        for value, expected in field_help_texts.items():
            with self.subTest(value=value):
                self.assertEqual(
                    task._meta.get_field(value).help_text, expected)

    def test_text_convert_to_slug(self):
        """El valor de title se convierte en slug."""
        task = TaskModelTest.task
        slug = task.slug
        self.assertEquals(slug, 'i-am-a-str'*10)

    def test_text_slug_max_length_not_exceed(self):
        """
        Un slug más largo se trunca para evitar que se supere el campo max_length del modelo de slug.
        """
        task = TaskModelTest.task
        max_length_slug = task._meta.get_field('slug').max_length
        length_slug = len(task.slug)
        self.assertEqual(max_length_slug, length_slug)

    def test_object_name_is_title_fild(self):
        """El campo __str__ del objeto task contiene el valor de la tarea.campo de título."""
        task = TaskModelTest.task
        expected_object_name = task.title
        self.assertEqual(expected_object_name, str(task))
