import shutil
import tempfile

from tasks.forms import TaskCreateForm
from tasks.models import Task
from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client, TestCase, override_settings
from django.urls import reverse

# Crea una carpeta temporal para los archivos multimedia
# Anularemos la carpeta de medios para la prueba
TEMP_MEDIA_ROOT = tempfile.mkdtemp(dir=settings.BASE_DIR)


# Utilizaremos la carpeta temporal TEMP_MEDIA_ROOT
# para guardar archivos multimedia durante la prueba, y luego la borraremos
@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class TaskCreateFormTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Crea un registro en la base de datos para validar el slug existente
        Task.objects.create(
            title='Título de prueba',
            text='Cuerpo de prueba',
            slug='first'
        )
        # Crea un formulario si necesitas validar los atributos
        cls.form = TaskCreateForm()

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        # shutil es una librería de Python con herramientas útiles
        # para gestionar archivos y directorios, incluyendo
        # crear, borrar, copiar, mover y editar
        # El método shutil.rmtree borra el directorio y todo su contenido
        shutil.rmtree(TEMP_MEDIA_ROOT, ignore_errors=True)

    def setUp(self):
        # Crea un cliente no autorizado
        self.guest_client = Client()

    def test_create_task(self):
        """Un formulario válido crea un registro en Task."""
        # Cuenta el número de registros en Task
        tasks_count = Task.objects.count()
        # Para probar la carga de imágenes,
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
            'título': 'Título de prueba',
            'texto': 'Cuerpo de prueba',
            'imagen': uploaded,
        }
        response = self.guest_client.post(
            reverse('tasks:home'),
            data=form_data,
            follow=True
        )
        # Prueba si la redirección funciona
        self.assertRedirects(response, reverse('tasks:task_added'))
        # Comprueba si ha aumentado el número de mensajes
        self.assertEqual(Task.objects.count(), tasks_count+1)
        # Comprueba que se ha creado el registro con el slug especificado
        self.assertTrue(
            Task.objects.filter(
                slug='testovyij-zagolovok',
                text='Cuerpo de prueba',
                image='tasks/small.gif'
                ).exists()
        )

    def test_cant_create_existing_slug(self):
        # Cuenta el número de registros en Task
        tasks_count = Task.objects.count()
        form_data = {
            'título': 'Título del formulario',
            'texto': 'Cuerpo del formulario',
            'slug': 'first',  # Intenta enviar un slug ya existente en la base de datos
        }
        # Envía una solicitud POST
        response = self.guest_client.post(
            reverse('tasks:home'),
            data=form_data,
            follow=True
        )
        # Asegúrate de que el registro de la base de datos no se ha creado
        # Compara el número de registros en Task antes y después de enviar el formulario
        self.assertEqual(Task.objects.count(), tasks_count)
        # Comprueba que el formulario devuelve un error apropiado:
        # toma el diccionario 'form' del objeto response
        # y especifica el error esperado para el campo 'slug' de este diccionario
        self.assertFormError(
            response,
            'form',
            'slug',
            'El slug " first" ya existe, introduce un slug único'
        )
        # Comprueba que la página no se ha bloqueado y que devuelve un código de estado 200.
        self.assertEqual(response.status_code, 200)

    # Si no ha probado el contenido de las etiquetas en los modelos
    # o redefinirlos al crear el formulario: probamos así:
    def test_title_label(self):
        title_label = TaskCreateFormTests.form.fields['title'].label
        self.assertEqual(title_label, 'Título')

    def test_title_help_text(self):
        title_help_text = TaskCreateFormTests.form.fields['title'].help_text
        self.assertEqual(title_help_text, 'Introduce el nombre de la tarea')
