from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator

from api.v1.discounts.models import StudentDiscount, TariffDiscount


class Tariff(models.Model):
    title = models.CharField(max_length=300)
    desc = models.CharField(max_length=500)
    days = models.PositiveSmallIntegerField(validators=[MinValueValidator(1)])
    price = models.PositiveIntegerField()
    tariff_discount = models.BooleanField(default=False)
    student_discount = models.BooleanField(default=True)
    tariff_discount_amount = models.FloatField(default=0)
    student_discount_amount = models.FloatField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def clean(self):
        if self.student_discount and not StudentDiscount.objects.exists():
            raise ValidationError({'student_discount': 'not found'})

        if self.tariff_discount and not TariffDiscount.objects.exists():
            raise ValidationError({'tariff_discount': 'not found'})

    def __str__(self):
        return f'Tariff: {self.days} days'
