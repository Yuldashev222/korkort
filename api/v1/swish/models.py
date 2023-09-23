from django.core.exceptions import ValidationError
from django.db import models
from django.core.cache import cache


class MinBonusMoney(models.Model):
    money = models.PositiveSmallIntegerField()

    def __str__(self):
        return str(self.money)

    def clean(self):
        if not self.pk and MinBonusMoney.objects.exists():
            raise ValidationError('obj exist')

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.set_redis()

    @classmethod
    def get_min_bonus_money(cls):
        temp = cache.get('min_bonus_money')
        if not temp:
            cls.set_redis()
            temp = cache.get('min_bonus_money')
        return temp

    @classmethod
    def set_redis(cls):
        cache.set('min_bonus_money', cls.objects.first(), 60 * 60 * 24 * 30)


class SwishCard(models.Model):
    number = models.PositiveSmallIntegerField(verbose_name='Swish Account')
    student = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    paid_at = models.DateTimeField(blank=True, null=True)
    is_paid = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']

    def clean(self):
        if self.is_paid and not self.paid_at:
            raise ValidationError({'paid_at': 'This field is required.'})

    def __str__(self):
        return str(self.number)
