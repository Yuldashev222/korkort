from django.db import models
from django.core.validators import MinValueValidator

from api.v1.general.services import normalize_text


class TariffAdvantage(models.Model):
    text = models.CharField(max_length=255)

    def __str__(self):
        return self.text

    def save(self, *args, **kwargs):
        self.text = normalize_text(self.text)
        super().save(*args, **kwargs)


class Tariff(models.Model):
    title = models.CharField(max_length=100)
    price = models.PositiveIntegerField()
    discount_price = models.PositiveIntegerField(default=0)
    day = models.PositiveSmallIntegerField(validators=[MinValueValidator(1)])
    image = models.ImageField(upload_to='tariffs/images/', blank=True, null=True)
    desc = models.CharField(max_length=255, blank=True)
    advantages = models.ManyToManyField(TariffAdvantage, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.title}'

    def save(self, *args, **kwargs):
        self.title = normalize_text(self.title)
        self.desc = normalize_text(self.desc)
        super().save(*args, **kwargs)
