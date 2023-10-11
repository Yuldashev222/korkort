from django.db import models
from django.core.cache import cache
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator

from api.v1.discounts.models import StudentDiscount, TariffDiscount


class Tariff(models.Model):
    days = models.PositiveSmallIntegerField(validators=[MinValueValidator(1)])
    price = models.PositiveIntegerField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    tariff_discount = models.BooleanField(default=False)
    tariff_discount_amount = models.FloatField(default=0)

    student_discount = models.BooleanField(default=True)
    student_discount_amount = models.FloatField(default=0)

    class Meta:
        ordering = ['-created_at']

    def clean(self):
        if self.student_discount and not StudentDiscount.objects.exists():
            raise ValidationError({'student_discount': 'not found'})

        if self.tariff_discount and not TariffDiscount.objects.exists():
            raise ValidationError({'tariff_discount': 'not found'})

    def __str__(self):
        return f'Tariff: {self.days} days'

    @classmethod
    def get_tariffs(cls):
        tariffs = cache.get('tariffs')
        if not tariffs:
            cls.set_redis()
            tariffs = cache.get('tariffs')
        return tariffs

    @classmethod
    def set_redis(cls):
        cache.set('tariffs', cls.objects.all())


class TariffDetail(models.Model):
    tariff = models.ForeignKey(Tariff, on_delete=models.CASCADE)
    language = models.ForeignKey('languages.Language', on_delete=models.PROTECT)
    title = models.CharField(max_length=300)
    desc = models.CharField(max_length=500, blank=True)

    class Meta:
        unique_together = ['tariff', 'language']

    @classmethod
    def get_tariff_details(cls):
        tariff_details = cache.get('tariff_details')
        if not tariff_details:
            cls.set_redis()
            tariff_details = cache.get('tariff_details')
        return tariff_details

    @classmethod
    def set_redis(cls):
        cache.set('tariff_details', cls.objects.values())

    def str(self):
        return self.title
