import string
import secrets
from django.db import models


class Order(models.Model):
    order_id = models.CharField(verbose_name='ID', unique=True, max_length=7)
    student = models.ForeignKey('accounts.CustomUser', verbose_name='Object', on_delete=models.SET_NULL,
                                null=True, related_name='orders')
    student_email = models.EmailField(verbose_name='Email')
    student_name = models.CharField(verbose_name='Name', max_length=200)
    student_bonus_amount = models.FloatField(verbose_name='bonus discount', default=0)
    use_bonus_money = models.BooleanField(verbose_name='Use Bonus', default=False)
    purchased_price = models.FloatField(default=0)

    student_discount_amount = models.FloatField(verbose_name='User Code discount', default=0)
    student_discount_value = models.PositiveIntegerField(default=0)
    student_discount_is_percent = models.BooleanField(default=False)

    tariff_discount_name = models.CharField(max_length=50, default='-')
    tariff_discount_amount = models.FloatField(verbose_name='Tariff Discount', default=0)
    tariff_discount_value = models.PositiveIntegerField(default=0)
    tariff_discount_is_percent = models.BooleanField(default=True)

    expire_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    purchased_at = models.DateTimeField(blank=True, null=True)

    is_paid = models.BooleanField(default=False)

    stripe_id = models.CharField(max_length=100, blank=True)
    stripe_url = models.URLField(blank=True)

    tariff = models.ForeignKey('tariffs.Tariff', verbose_name='Object', on_delete=models.SET_NULL, null=True)
    tariff_price = models.PositiveIntegerField(verbose_name='Price')
    tariff_days = models.PositiveSmallIntegerField(verbose_name='Days')

    called_student = models.ForeignKey('accounts.CustomUser', verbose_name='Object', null=True,
                                       on_delete=models.SET_NULL)
    called_student_code = models.CharField(verbose_name='User Code', max_length=6, default='-')
    called_student_email = models.EmailField(verbose_name='Email', blank=True)
    called_student_name = models.CharField(verbose_name='Name', max_length=200, default='-')
    called_student_bonus_added = models.BooleanField(verbose_name='Bonus Added', default=False)

    def __str__(self):
        return self.order_id

    @property
    def generate_unique_order_id(self):
        while True:
            value = ''.join(secrets.choice(string.digits) for _ in range(7))
            if not Order.objects.filter(order_id=value).exists():
                return value
