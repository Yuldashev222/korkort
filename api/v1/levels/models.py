from django.db import models
from django.core.cache import cache
from django.core.validators import MinValueValidator
from rest_framework.exceptions import ValidationError

from api.v1.general.services import normalize_text


class Level(models.Model):
    correct_answers = models.PositiveSmallIntegerField(unique=True)
    ordering_number = models.PositiveSmallIntegerField(validators=[MinValueValidator(1)], unique=True)

    def __str__(self):
        return str(self.ordering_number)

    class Meta:
        ordering = ['ordering_number']

    def clean(self):
        if not self.pk and Level.objects.filter(ordering_number__lt=self.ordering_number,
                                                correct_answers__gt=self.correct_answers).exists():
            raise ValidationError({'correct_answers': 'error'})

    @classmethod
    def get_levels(cls):
        levels = cache.get('levels')
        if not levels:
            cls.set_redis()
            levels = cache.get('levels')
        return levels

    @classmethod
    def set_redis(cls):
        cache.set('levels', cls.objects.values().order_by('ordering_number'))


class LevelDetail(models.Model):
    level = models.ForeignKey(Level, on_delete=models.CASCADE)
    language = models.ForeignKey('languages.Language', on_delete=models.PROTECT)
    name = models.CharField(max_length=100)
    desc = models.CharField(max_length=300, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        unique_together = ['level', 'language']

    def save(self, *args, **kwargs):
        self.name = normalize_text(self.name)[0]
        super().save(*args, **kwargs)
