from django.db import models
from django.core.validators import MinValueValidator
from rest_framework.exceptions import ValidationError

from api.v1.general.services import normalize_text


class Level(models.Model):
    ordering_number = models.PositiveSmallIntegerField(primary_key=True, unique=True, validators=[MinValueValidator(1)])
    correct_answers = models.PositiveSmallIntegerField(unique=True)

    def __str__(self):
        return f'Level No {self.ordering_number}'

    def clean(self):
        if not self.pk and Level.objects.filter(ordering_number__lt=self.ordering_number,
                                                correct_answers__gt=self.correct_answers).exists():
            raise ValidationError({'correct_answers': 'error'})


class LevelDetail(models.Model):
    level = models.ForeignKey(Level, on_delete=models.CASCADE)
    language = models.ForeignKey('languages.Language', on_delete=models.PROTECT)
    name = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.language_id} Level No {self.level_id}'

    class Meta:
        unique_together = ['level', 'language']

    def save(self, *args, **kwargs):
        self.name = normalize_text(self.name)[0]
        super().save(*args, **kwargs)
