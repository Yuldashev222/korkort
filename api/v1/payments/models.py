import string
import secrets
from datetime import timedelta
from django.db import models
from django.conf import settings
from django.utils.timezone import now


class Order(models.Model):
    order_id = models.CharField(verbose_name='ID', max_length=7)
    student = models.ForeignKey('accounts.CustomUser', on_delete=models.SET_NULL, null=True, related_name='orders')
    student_email = models.EmailField()
    student_bonus_amount = models.FloatField(verbose_name='bonus amount', default=0)
    student_discount_amount = models.FloatField(default=0)
    student_discount_value = models.PositiveIntegerField(default=0)
    student_discount_is_percent = models.BooleanField(default=False)

    expire_at = models.DateTimeField(blank=True, null=True)
    purchased_at = models.DateTimeField(blank=True, null=True)
    purchased_price = models.FloatField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    is_paid = models.BooleanField(default=False)
    use_bonus_money = models.BooleanField(verbose_name='use bonus', default=False)

    stripe_id = models.CharField(max_length=100, blank=True)
    payment_link = models.URLField(blank=True, null=True)
    stripe_url = models.URLField(blank=True)

    tariff = models.ForeignKey('tariffs.Tariff', on_delete=models.SET_NULL, null=True)
    tariff_title = models.CharField(max_length=100)
    tariff_price = models.PositiveIntegerField()
    tariff_days = models.PositiveSmallIntegerField()

    tariff_discount_title = models.CharField(max_length=200, default='-')
    tariff_discount_amount = models.FloatField(default=0)
    tariff_discount_value = models.PositiveIntegerField(default=0)
    tariff_discount_is_percent = models.BooleanField(default=True)

    called_student = models.ForeignKey('accounts.CustomUser', on_delete=models.SET_NULL, null=True, blank=True)
    called_student_code = models.CharField(max_length=6, default='-')
    called_student_email = models.EmailField(blank=True)
    called_student_bonus_added = models.BooleanField(default=False)

    class Meta:
        ordering = ['-id']

    @classmethod
    def expire_orders(cls):
        return cls.objects.filter(created_at__lte=now() - timedelta(minutes=settings.STRIPE_CHECKOUT_TIMEOUT),
                                  is_paid=False)

    @property
    def generate_unique_order_id(self):
        while True:
            value = ''.join(secrets.choice(string.digits) for _ in range(7))
            if not Order.objects.filter(order_id=value).exists():
                return value
