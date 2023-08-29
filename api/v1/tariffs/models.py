from django.db import models
from django.core.cache import cache
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.utils.timezone import now

from api.v1.discounts.models import StudentDiscount, TariffDiscount
from api.v1.general.services import normalize_text


class TariffInfo(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='tariffs/images/', blank=True, null=True)
    desc = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f'{self.title}'

    def save(self, *args, **kwargs):
        self.desc, self.title = normalize_text(self.desc, self.title)
        super().save(*args, **kwargs)


class Tariff(models.Model):
    tariff_info = models.ForeignKey(TariffInfo, on_delete=models.CASCADE)
    day = models.PositiveSmallIntegerField(validators=[MinValueValidator(1)])
    price = models.PositiveIntegerField()
    tariff_discount = models.BooleanField(default=False)
    student_discount = models.BooleanField(default=True)
    tariff_discount_amount = models.FloatField(default=0)
    student_discount_amount = models.FloatField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        if self.student_discount and not StudentDiscount.objects.exists():
            raise ValidationError({'student_discount': 'not found'})

        if self.tariff_discount and not TariffDiscount.objects.exists():
            raise ValidationError({'tariff_discount': 'not found'})

    def __str__(self):
        return f'Tariff: {self.day} days'

    def save(self, *args, **kwargs):
        for field in ['tariff_discount', 'student_discount']:
            if getattr(self, field):
                discount = cache.get(field)
                if not discount:
                    if field == 'tariff_discount':
                        TariffDiscount.set_redis()
                    else:
                        StudentDiscount.set_redis()
                    discount = cache.get(field)

                if not discount or discount.get('valid_to') and discount['valid_to'] <= now().date():
                    setattr(self, field + '_amount', 0)
                    setattr(self, field, False)
                else:
                    if discount['is_percent']:
                        value = self.price * discount['discount_value'] / 100
                        setattr(self, field + '_amount', value)
                        setattr(self, field + '_amount', round(value, 1))
                    else:
                        setattr(self, field + '_amount', discount['discount_value'])

            else:
                setattr(self, field + '_amount', 0)

        super().save(*args, **kwargs)
