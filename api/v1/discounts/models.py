from django.db import models
from django.core.cache import cache
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator


class DiscountMixin(models.Model):
    title = models.CharField(max_length=200, blank=True)
    discount_value = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    is_percent = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        if self.is_percent and self.discount_value > 100:
            raise ValidationError({'discount_value': 'Enter the percent value'})

    def __str__(self):
        if self.is_percent:
            return f'{self.title}: {self.discount_value} %'
        return f'{self.title}: {self.discount_value} SEK'

    class Meta:
        abstract = True


class TariffDiscount(DiscountMixin):
    valid_from = models.DateTimeField(blank=True, null=True)
    valid_to = models.DateTimeField(blank=True, null=True)

    def clean(self):
        if self.valid_from and not self.valid_to:
            raise ValidationError({'valid_to': 'This field is required.'})

        if not self.valid_from and self.valid_to:
            raise ValidationError({'valid_from': 'This field is required.'})

        if self.valid_from and self.valid_to and self.valid_from > self.valid_to:
            raise ValidationError({'valid_from': 'the start time must be less than the end time.'})

    def save(self, *args, **kwargs):
        if self.pk:
            for tariff in self.tariff_set.all():
                tariff.save()
        super().save(*args, **kwargs)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['discount_value', 'is_percent'], name='unique discounts')
        ]


class StudentDiscount(DiscountMixin):
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        StudentDiscount.set_redis()

    @classmethod
    def set_redis(cls):
        obj = cls.objects.first()
        if obj:
            cache.set('student_discount', {'is_percent': obj.is_percent, 'discount_value': obj.discount_value})
