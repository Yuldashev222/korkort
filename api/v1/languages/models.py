from django.db import models
from django.core.cache import cache
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator


class Language(models.Model):
    language_id = models.CharField(primary_key=True, unique=True, max_length=4)
    name = models.CharField(max_length=100)
    ordering_number = models.PositiveSmallIntegerField(validators=[MinValueValidator(1)], unique=True)
    is_active = models.BooleanField(default=True)

    def clean(self):
        normalize_id = ''.join(self.language_id.split()).lower()
        if normalize_id != self.language_id or not normalize_id.isalpha():
            raise ValidationError({'language_id': 'enter the valid id'})

    def save(self, *args, **kwargs):
        self.language_id = ''.join(self.language_id.split()).lower()
        super().save(*args, **kwargs)

    @classmethod
    def get_languages(cls):
        languages = cache.get('languages')
        if languages is None:
            cls.set_redis()
            languages = cache.get('languages')
        return languages

    @classmethod
    def set_redis(cls):
        cache.set('languages', list(cls.objects.filter(is_active=True).values_list('language_id', flat=True)))

    class Meta:
        ordering = ['ordering_number']

    def __str__(self):
        return self.name
