from django.db import models
from django.core.exceptions import ValidationError


class Level(models.Model):
    car = models.ImageField(upload_to='levels/cars/', blank=True, null=True)
    title = models.CharField(max_length=200)
    level = models.PositiveSmallIntegerField(unique=True)

    def clean(self):
        if not Level.objects.filter(level=self.level - 1).exists():
            raise ValidationError({'level': f'{self.level - 1} level not found'})

    def save(self, *args, **kwargs):
        self.title = ' '.join(self.title.split())
        super().save(*args, **kwargs)
