from django.db import models
from django.core.cache import cache
from django.utils.timezone import now
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator


class MinBonusMoney(models.Model):
    money = models.PositiveSmallIntegerField(validators=[MinValueValidator(10)])

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

    student = models.ForeignKey('accounts.CustomUser', on_delete=models.SET_NULL, null=True)
    student_email = models.EmailField()
    student_name = models.CharField(max_length=200)
    student_money = models.FloatField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    paid_at = models.DateTimeField(blank=True, null=True)

    is_paid = models.BooleanField(default=False)

    def clean(self):
        if self.pk and not self.is_paid and SwishCard.objects.get(pk=self.pk).is_paid:
            raise ValidationError({'is_paid': 'not change'})

    def __str__(self):
        return str(self.number)

    def save(self, *args, **kwargs):
        if self.student:
            if not self.student_name:
                self.student_name = self.student.name

            if not self.student_email:
                self.student_email = self.student.email

            if self.student_money == 0:
                self.student_money = self.student.bonus_money
                self.student.bonus_money = 0
                self.student.save()

        if self.pk and self.is_paid and not SwishCard.objects.get(pk=self.pk).is_paid:
            self.paid_at = now()

        super().save(*args, **kwargs)
