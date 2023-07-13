from datetime import timedelta

from django.db import models
from django.utils.timezone import now


class Order(models.Model):
    student = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE)
    tariff = models.ForeignKey('tariffs.Tariff', on_delete=models.PROTECT)
    expire_at = models.DateTimeField()
    purchased_at = models.DateTimeField(auto_now_add=True)
    purchased_price = models.PositiveIntegerField()

    tariff_title = models.CharField(max_length=100)
    tariff_price = models.PositiveIntegerField()
    tariff_discount_price = models.PositiveIntegerField()
    tariff_day = models.PositiveSmallIntegerField()
    tariff_advantages = models.TextField(default='')

    @classmethod
    def active_orders(cls):
        return cls.objects.filter(expire_at__gt=now())

    def save(self, *args, **kwargs):
        if not self.pk:
            for advantage in self.tariff.advantages.all():
                self.tariff_advantages += str(advantage.text) + '\n'
            self.tariff_advantages = self.tariff_advantages.rstrip()

        self.tariff_day = self.tariff.day
        self.tariff_title = self.tariff.title
        self.tariff_price = self.tariff.price
        self.expire_at = now() + timedelta(days=self.tariff_day)
        self.tariff_discount_price = self.tariff.discount_price
        self.purchased_price = self.tariff_price - self.tariff_discount_price
        super().save(*args, **kwargs)
