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
    def get_level_correct_counts(cls):
        level_correct_counts = cache.get('level_correct_counts')
        if not level_correct_counts:
            cls.set_redis()
            level_correct_counts = cache.get('level_correct_counts')
        return level_correct_counts

    @classmethod
    def set_redis(cls):
        counts = list(cls.objects.values_list('correct_answers', flat=True).order_by('correct_answers'))
        cache.set('level_correct_counts', counts)


class LevelDetail(models.Model):
    level = models.ForeignKey(Level, on_delete=models.CASCADE)
    language = models.ForeignKey('languages.Language', on_delete=models.PROTECT)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['level__ordering_number']
        unique_together = ['level', 'language']

    def save(self, *args, **kwargs):
        self.name = normalize_text(self.name)[0]
        super().save(*args, **kwargs)
