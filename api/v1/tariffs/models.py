from django.db import models
from django.core.cache import cache
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator

from api.v1.discounts.models import StudentDiscount
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
    discount = models.ForeignKey('discounts.TariffDiscount', on_delete=models.PROTECT, blank=True, null=True)
    tariff_discount_amount = models.FloatField(default=0)
    student_discount_amount = models.FloatField(default=0)
    student_discount = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        if self.student_discount and not StudentDiscount.objects.exists():
            raise ValidationError({'student_discount': 'not found'})

    def __str__(self):
        return f'Tariff: {self.day} days'

    def save(self, *args, **kwargs):
        discount = self.discount
        if discount:
            self.tariff_discount_amount = discount.discount_value
            if discount.is_percent:
                self.tariff_discount_amount = self.price * discount.discount_value / 100
                self.tariff_discount_amount = round(self.tariff_discount_amount, 1)
        else:
            self.tariff_discount_amount = 0

        if self.student_discount:
            student_discount = cache.get('student_discount')
            if not student_discount:
                StudentDiscount.set_redis()
                student_discount = cache.get('student_discount')

            if student_discount:
                if student_discount['is_percent']:
                    self.student_discount_amount = self.price * student_discount['discount_value'] / 100
                    self.student_discount_amount = round(self.student_discount_amount, 1)
                else:
                    self.student_discount_amount = student_discount['discount_value']
            else:
                self.student_discount_amount = 0
                self.student_discount = False
        else:
            self.student_discount_amount = 0

        super().save(*args, **kwargs)
