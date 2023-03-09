from django.db import models
# Necesitas instalar la librería pytils: pip install pytils.
from pytils.translit import slugify


class Task(models.Model):
    title = models.CharField(
        'Título',
        default='Valores predeterminados',
        max_length=100,
        help_text='Introduce el nombre de la tarea'
    )
    text = models.TextField(
        'Texto',
        help_text='Introduce la descripción de la tarea'
    )
    slug = models.SlugField(
        'El slug de la URL para la página de la tarea',
        max_length=100,
        unique=True,
        blank=True,
        help_text=('Introduce una URL única para la página de la tarea. Utiliza solo '
                   'Caracteres latinos, números, guiones y guiones bajos')
    )
    image = models.ImageField(
        'Imagen',
        upload_to='tasks/',
        blank=True,
        null=True,
        help_text='Sube una imagen'
    )

    def __str__(self):
        return self.title

    # Amplía el método save() por defecto: si no se especifica el campo slug,
    # transliterar el valor del campo del título en caracteres latinos (100 caracteres como máximo)
    # (100 characters max)
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)[:100]
        super().save(*args, **kwargs)
