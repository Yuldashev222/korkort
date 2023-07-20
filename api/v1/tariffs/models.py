from django.core.exceptions import ValidationError
from django.db import models
from django.core.validators import MinValueValidator

from api.v1.discounts.models import StudentDiscount
from api.v1.general.services import normalize_text


class Tariff(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='tariffs/images/', blank=True, null=True)
    desc = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f'{self.title}'

    # def clean(self):
    #     if not self.tariffday_set.exists():
    #         raise ValidationError('tariff day required')

    def save(self, *args, **kwargs):
        self.desc = normalize_text(self.desc)
        self.title = normalize_text(self.title)
        super().save(*args, **kwargs)


class TariffDay(models.Model):
    tariff = models.ForeignKey(Tariff, on_delete=models.CASCADE)
    day = models.PositiveSmallIntegerField(validators=[MinValueValidator(1)])
    price = models.PositiveIntegerField()
    discount = models.ForeignKey('discounts.TariffDiscount', on_delete=models.PROTECT, blank=True, null=True)
    discount_price = models.PositiveIntegerField(default=0)
    student_discount_price = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if self.discount:
            if not self.discount.is_percent:
                self.discount_price = self.discount.discount_value
            else:
                self.discount_price = self.price * self.discount.discount_value / 100

            self.discount_price = round(self.discount_price, 1)
        else:
            self.discount_price = 0  # last

        student_discount = StudentDiscount.objects.first()
        if student_discount and student_discount.is_active:
            if not student_discount.is_percent:
                self.student_discount_price = student_discount.discount_value
            else:
                self.student_discount_price = self.price * student_discount.discount_value / 100

            self.student_discount_price = round(self.student_discount_price, 1)
        else:
            self.student_discount_price = 0  # last

        super().save(*args, **kwargs)

    def __str__(self):
        return f'Tariff: {self.day} days'
