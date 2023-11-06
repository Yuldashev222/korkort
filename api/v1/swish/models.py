from django.db import models
from django.core.cache import cache
from django.utils.timezone import now
from django.core.exceptions import ValidationError


class MinBonusMoney(models.Model):
    money = models.PositiveSmallIntegerField()

    def __str__(self):
        return str(self.money)

    def clean(self):
        if not self.pk and MinBonusMoney.objects.exists():
            raise ValidationError('obj exist')

    @classmethod
    def get_min_bonus_money(cls):
        temp = cache.get('min_bonus_money')
        if temp is None:
            cls.set_redis()
            temp = cache.get('min_bonus_money')
        return temp

    @classmethod
    def set_redis(cls):
        obj = cls.objects.first()
        if obj:
            cache.set('min_bonus_money', obj.money)
        else:
            cache.delete('min_bonus_money')


class SwishCard(models.Model):
    number = models.CharField(max_length=50, verbose_name='Swish Account')
    student = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    paid_at = models.DateTimeField(blank=True, null=True)
    is_paid = models.BooleanField(default=False)
    student_money = models.FloatField(default=0)

    def clean(self):
        if self.pk and not self.is_paid and SwishCard.objects.get(pk=self.pk).is_paid:
            raise ValidationError({'is_paid': 'not change'})

        if self.is_paid and not self.paid_at:
            raise ValidationError({'paid_at': 'This field is required.'})

    def __str__(self):
        return str(self.number)

    def save(self, *args, **kwargs):
        if self.student_money == 0 and self.student:
            self.student_money = self.student.bonus_money
        if self.pk and self.is_paid and not SwishCard.objects.get(pk=self.pk).is_paid:
            self.paid_at = now()
        super().save(*args, **kwargs)
