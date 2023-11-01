from django.db import models
from django.core.cache import cache
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator


class Language(models.Model):
    name = models.CharField(max_length=100)
    ordering_number = models.PositiveSmallIntegerField(validators=[MinValueValidator(1)], unique=True)
    is_active = models.BooleanField(default=True)

    @classmethod
    def get_languages(cls):
        languages = cache.get('languages')
        if languages is None:
            cls.set_redis()
            languages = cache.get('languages')
        return languages

    @classmethod
    def set_redis(cls):
        cache.set(
            'languages',
            list(map(str, cls.objects.filter(is_active=True).values_list('pk', flat=True).order_by('ordering_number')))
        )

    def __str__(self):
        return self.name
