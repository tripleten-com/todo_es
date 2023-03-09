from django import forms
from django.core.exceptions import ValidationError
from pytils.translit import slugify

from .models import Task


class TaskCreateForm(forms.ModelForm):
    """Formulario para crear una tarea."""
    class Meta:
        model = Task
        # La magia de Django: '__all__' se utiliza para crear una tupla de todos los campos del modelo;
        # labels y help_texts se recuperan de los campos del modelo
        fields = '__all__'

    # Validar el campo slug
    def clean_slug(self):
        """Procesa los casos en los que el slug no es único."""
        cleaned_data = super().clean()
        slug = cleaned_data['slug']
        if not slug:
            title = cleaned_data['title']
            slug = slugify(title)[:100]
        if Task.objects.filter(slug=slug).exists():
            raise ValidationError(f'El slug "{slug}" ya existe, '
                                  'introduce un valor único')
        return slug
