from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator


class Level(models.Model):
    title_en = models.CharField(max_length=200, blank=True)
    title_swe = models.CharField(max_length=200, blank=True)
    title_easy_swe = models.CharField(max_length=200, blank=True)
    car = models.ImageField(upload_to='levels/cars/', blank=True, null=True)
    level = models.PositiveSmallIntegerField(unique=True, validators=[MinValueValidator(1)])

    def clean(self):
        if self.level == 1:
            raise ValidationError({'level': 'already exists.'})
        if self.level != 1 and not Level.objects.filter(level=self.level - 1).exists():
            raise ValidationError({'level': f'{self.level - 1} level not found'})

    def save(self, *args, **kwargs):
        self.title = ' '.join(self.title_en.split())
        self.title = ' '.join(self.title_swe.split())
        self.title = ' '.join(self.title_easy_swe.split())
        super().save(*args, **kwargs)
