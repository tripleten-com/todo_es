from django import forms
from django.core.exceptions import ValidationError
from pytils.translit import slugify

from .models import Task


class TaskCreateForm(forms.ModelForm):
    """Form for creating a task."""
    class Meta:
        model = Task
        # Django magic: '__all__' is used to create a tuple of all model fields;
        # labels and help_texts are retrieved from the model fields
        fields = '__all__'

    # Валидация поля slug
    def clean_slug(self):
        """Processes the cases where slug is not unique."""
        cleaned_data = super().clean()
        slug = cleaned_data['slug']
        if not slug:
            title = cleaned_data['title']
            slug = slugify(title)[:100]
        if Task.objects.filter(slug=slug).exists():
            raise ValidationError(f'Slug "{slug}" already exists, '
                                  'enter a unique value')
        return slug
