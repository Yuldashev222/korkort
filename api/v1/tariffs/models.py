from django.db import models
from django.core.validators import MinValueValidator


class Tariff(models.Model):
    days = models.PositiveSmallIntegerField(validators=[MinValueValidator(1)], unique=True)
    price = models.PositiveIntegerField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f'Tariff: {self.days} days'
