from django.db import models
from django.core.cache import cache
from django.core.validators import MinValueValidator

from api.v1.general.services import normalize_text


class Language(models.Model):
    name = models.CharField(max_length=100)

    @classmethod
    def get_languages(cls):
        languages = cache.get('languages')
        if languages is None:
            cls.set_redis()
            languages = cache.get('languages')
        return languages

    @classmethod
    def set_redis(cls):
        cache.set('languages', cls.objects.values_list('pk', flat=True))

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.name = normalize_text(self.name)[0]
        super().save(*args, **kwargs)
