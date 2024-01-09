from django.db import models
from django_ckeditor_5.fields import CKEditor5Field
from django.core.validators import MinValueValidator

from api.v1.general.services import normalize_text


class Todo(models.Model):
    ordering_number = models.PositiveSmallIntegerField(primary_key=True, unique=True, validators=[MinValueValidator(1)])

    def __str__(self):
        return f'Todo No {self.ordering_number}'


class TodoDetail(models.Model):
    todo = models.ForeignKey(Todo, on_delete=models.CASCADE)
    language = models.ForeignKey('languages.Language', on_delete=models.PROTECT)
    title = models.CharField(max_length=300)
    text = CKEditor5Field(max_length=500)

    def __str__(self):
        return self.title

    class Meta:
        unique_together = ['todo', 'language']
        verbose_name = 'Todo Language'
        verbose_name_plural = 'Todo Languages'

    def save(self, *args, **kwargs):
        self.title = normalize_text(self.title)[0]
        super().save(*args, **kwargs)


class TodoStudent(models.Model):
    todo = models.ForeignKey(Todo, on_delete=models.CASCADE)
    student = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE)
    is_completed = models.BooleanField(default=True)
