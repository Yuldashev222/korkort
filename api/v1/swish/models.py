from django.core.cache import cache
from django.db import models


class MinBonusMoney(models.Model):
    money = models.PositiveSmallIntegerField()

    def __str__(self):
        return str(self.money)

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
    number = models.PositiveSmallIntegerField()
    student = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    is_paid = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return str(self.number)
