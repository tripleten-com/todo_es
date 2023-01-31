from django.db import models
# You need to install the pytils library: pip install pytils.
from pytils.translit import slugify


class Task(models.Model):
    title = models.CharField(
        'Title',
        default='Default value',
        max_length=100,
        help_text='Enter task name'
    )
    text = models.TextField(
        'Текст',
        help_text='Enter task description'
    )
    slug = models.SlugField(
        'URL slug for the task page',
        max_length=100,
        unique=True,
        blank=True,
        help_text=('Enter a unique URL for the task page. Use only '
                   'Latin characters, numbers, hyphens, and underscores')
    )
    image = models.ImageField(
        'Image',
        upload_to='tasks/',
        blank=True,
        null=True,
        help_text='Upload an image'
    )

    def __str__(self):
        return self.title

    # Extend the default save() method: if the slug field is not specified,
    # transliterate the title field value as Latin characters
    # (100 characters max)
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)[:100]
        super().save(*args, **kwargs)
