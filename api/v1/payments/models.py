from datetime import timedelta

from django.db import models
from django.conf import settings
from django.core.cache import cache
from django.utils.timezone import now

from api.v1.discounts.models import StudentDiscount


class Order(models.Model):
    student = models.ForeignKey('accounts.CustomUser', on_delete=models.SET_NULL, null=True, related_name='orders')
    student_email = models.EmailField(editable=False)
    student_bonus_amount = models.FloatField(default=0)
    student_discount_amount = models.FloatField(default=0)
    student_discount_value = models.PositiveIntegerField(default=0)
    student_discount_is_percent = models.BooleanField(default=True)

    expire_at = models.DateTimeField(blank=True, null=True)
    purchased_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    is_paid = models.BooleanField(default=False)
    use_bonus_money = models.BooleanField(default=False)

    stripe_id = models.CharField(max_length=100, blank=True)
    payment_link = models.URLField(blank=True, null=True)
    stripe_url = models.URLField(blank=True)

    tariff = models.ForeignKey('tariffs.Tariff', on_delete=models.SET_NULL, null=True)
    tariff_title = models.CharField(max_length=100, editable=False)
    tariff_price = models.PositiveIntegerField(editable=False)
    tariff_day = models.PositiveSmallIntegerField(editable=False)

    tariff_discount = models.ForeignKey('discounts.TariffDiscount', on_delete=models.SET_NULL, blank=True, null=True)
    tariff_discount_title = models.CharField(max_length=200, blank=True, editable=False)
    tariff_discount_amount = models.FloatField(default=0, editable=False)
    tariff_discount_value = models.PositiveIntegerField(default=0, editable=False)
    tariff_discount_is_percent = models.BooleanField(default=True, editable=False)

    called_student = models.ForeignKey('accounts.CustomUser', on_delete=models.SET_NULL, null=True, blank=True)
    called_student_code = models.CharField(max_length=6, blank=True, editable=False)
    called_student_email = models.EmailField(blank=True, editable=False)
    called_student_bonus_added = models.BooleanField(default=False, editable=False)

    @classmethod
    def delete_student_expire_orders(cls):
        cls.objects.filter(is_paid=False, created_at__gt=now() - timedelta(minutes=10)).delete()

    def save(self, *args, **kwargs):
        tariff = self.tariff
        discount = self.tariff.discount
        student = self.student
        called_student = self.called_student
        if not self.pk:
            self.student_email = student.email

            self.tariff_title = tariff.tariff_info.title
            self.tariff_price = tariff.price
            self.tariff_day = tariff.day

            if discount:
                self.tariff_discount = discount
                self.tariff_discount_value = discount.discount_value
                self.tariff_discount_title = discount.title
                self.tariff_discount_is_percent = discount.is_percent
                self.tariff_discount_amount = tariff.tariff_discount_amount

            if tariff.student_discount:
                student_discount = cache.get('student_discount')
                if not student_discount:
                    StudentDiscount.set_redis()
                    student_discount = cache.get('student_discount')

                if student_discount:
                    self.student_discount_value = student_discount.get('discount_value')
                    self.student_discount_is_percent = student_discount.get('is_percent')
                    self.student_discount_amount = tariff.student_discount_amount

            if called_student:
                self.called_student_code = called_student.user_code
                self.called_student_email = called_student.email

            if self.use_bonus_money and student.bonus_money > 0:
                remaining_amount = self.tariff_price - (self.student_discount_amount + self.tariff_discount_amount)
                if remaining_amount > 0:
                    if student.bonus_money >= remaining_amount:
                        student.bonus_money -= remaining_amount
                        self.student_bonus_amount = remaining_amount
                    else:
                        self.student_bonus_amount = student.bonus_money
                        student.bonus_money = 0
                    student.save()

        all_discounts = self.student_discount_amount + self.tariff_discount_amount + self.student_bonus_amount
        if self.tariff_price - all_discounts <= 0:
            self.is_paid = True

        if self.is_paid:
            self.purchased_at = now()
            self.expire_at = self.purchased_at + timedelta(days=self.tariff_day)

            if self.called_student and not self.called_student_bonus_added:
                called_student = self.called_student
                called_student.bonus_money += round(self.student_discount_amount, 1)
                called_student.save()
                self.called_student_bonus_added = True

            if self.stripe_id and not self.stripe_url:
                if '_test_' in settings.STRIPE_SECRET_KEY:
                    path = '/test/'
                else:
                    path = '/'
                self.stripe_url = f'https://dashboard.stripe.com{path}payments/{self.stripe_id}'

        super().save(*args, **kwargs)
