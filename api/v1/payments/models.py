from datetime import timedelta

from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils.timezone import now

from api.v1.accounts.models import StudentCalledEmail
from api.v1.discounts.models import StudentDiscount


class Order(models.Model):
    student_email = models.EmailField()
    student_bonus_price = models.PositiveIntegerField(default=0)
    student = models.ForeignKey('accounts.CustomUser', on_delete=models.SET_NULL, null=True,
                                related_name='orders')

    expire_at = models.DateTimeField(blank=True, null=True)
    purchased_at = models.DateTimeField(blank=True, null=True)
    purchased_price = models.PositiveIntegerField(default=0)
    is_paid = models.BooleanField(default=False)

    stripe_id = models.CharField(max_length=100, blank=True)
    stripe_url = models.URLField(blank=True)

    tariff = models.ForeignKey('tariffs.TariffDay', on_delete=models.SET_NULL, null=True)
    tariff_title = models.CharField(max_length=100)
    tariff_price = models.PositiveIntegerField()
    tariff_day = models.PositiveSmallIntegerField()

    tariff_discount = models.ForeignKey('discounts.TariffDiscount', on_delete=models.SET_NULL, blank=True, null=True)
    tariff_discount_value = models.PositiveIntegerField(default=0)
    tariff_discount_is_percent = models.BooleanField(default=False)

    called_student = models.ForeignKey('accounts.CustomUser', on_delete=models.SET_NULL, null=True, blank=True)
    called_student_code = models.CharField(max_length=6, blank=True)
    called_student_email = models.EmailField(blank=True)
    student_discount_price = models.PositiveIntegerField(default=0)

    def save(self, *args, **kwargs):
        tariff = self.tariff
        discount = self.tariff.discount
        student = self.student
        if not self.pk:
            self.student_email = student.email

            self.tariff_title = tariff.tariff.title
            self.tariff_price = tariff.price
            self.tariff_day = tariff.day

            self.purchased_price = self.tariff_price

            if discount:
                self.tariff_discount = discount
                self.tariff_discount_value = discount.discount_value
                self.tariff_discount_is_percent = discount.is_percent
                self.purchased_price -= tariff.discount_price

            if self.called_student_code:
                self.called_student = get_user_model().objects.get(user_code=self.called_student_code)
                self.called_student_email = self.called_student.email
                self.student_discount_price = tariff.student_discount_price
                self.purchased_price -= self.student_discount_price

            if self.purchased_price > 0:
                student_bonus_price = student.bonus_price
                if student_bonus_price > 0:
                    if self.purchased_price - student_bonus_price > 0:
                        self.purchased_price -= student_bonus_price
                        student.bonus_price = 0
                        self.student_bonus_price = student_bonus_price
                    else:
                        student.bonus_price -= self.purchased_price
                        self.student_bonus_price = self.purchased_price
                        self.purchased_price = 0
                        self.is_paid = True

                    student.save()
            else:
                self.is_paid = True

        if self.is_paid:
            self.purchased_at = now()
            self.expire_at = self.purchased_at + timedelta(days=self.tariff_day)

            if self.called_student and not StudentCalledEmail.objects.filter(email=self.called_student_email,
                                                                             student_id=self.student_id).exists():
                StudentCalledEmail.objects.create(student=self.student, email=self.called_student_email)
                self.called_student.bonus_price += self.student_discount_price
                self.called_student.save()

        if self.stripe_id and not self.stripe_url:
            if '_test_' in settings.STRIPE_SECRET_KEY:
                path = '/test/'
            else:
                path = '/'
            self.stripe_url = f'https://dashboard.stripe.com{path}payments/{self.stripe_id}'

        self.purchased_price = round(self.purchased_price, 1)
        super().save(*args, **kwargs)
