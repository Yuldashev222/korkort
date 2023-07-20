from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models


class DiscountMixin(models.Model):
    discount_value = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    is_percent = models.BooleanField(default=True)
    discount_title = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        if self.is_percent and self.discount_value > 100:
            raise ValidationError({'discount_value': 'Enter the percent value'})

    def __str__(self):
        if self.is_percent:
            return f'{self.discount_value} %'
        return f'{self.discount_value} SEK'

    class Meta:
        abstract = True


class TariffDiscount(DiscountMixin):
    def save(self, *args, **kwargs):
        if self.pk:
            for tariff in self.tariffday_set.all():
                tariff.save()
        super().save(*args, **kwargs)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['discount_value', 'is_percent'], name='unique discounts')
        ]


class StudentDiscount(DiscountMixin):
    is_active = models.BooleanField(default=True)
