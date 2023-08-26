from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator

from api.v1.general.services import normalize_text


class Level(models.Model):
    title_en = models.CharField(max_length=200, blank=True)
    title_swe = models.CharField(max_length=200, blank=True)
    title_e_swe = models.CharField(max_length=200, blank=True)
    level = models.PositiveSmallIntegerField(unique=True, validators=[MinValueValidator(1)])

    def clean(self):
        if self.level == 1:
            raise ValidationError({'level': 'already exists.'})
        if self.level != 1 and not Level.objects.filter(level=self.level - 1).exists():
            raise ValidationError({'level': f'{self.level - 1} level not found'})

    def save(self, *args, **kwargs):
        self.title_en, self.title_swe, self.title_e_swe = normalize_text(self.title_en, self.title_swe,
                                                                         self.title_e_swe)
        super().save(*args, **kwargs)
