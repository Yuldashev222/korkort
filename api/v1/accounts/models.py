import string
import secrets

from datetime import timedelta

from django.db import models
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.password_validation import validate_password

from api.v1.general.services import normalize_text

from .managers import CustomUserManager


class CustomUser(AbstractUser):
    username = None
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = CustomUserManager()

    email = models.EmailField(_("email address"), unique=True)
    password = models.CharField(_("password"), max_length=128, validators=[validate_password])
    first_name = models.CharField(_("first name"), max_length=50)
    last_name = models.CharField(_("last name"), max_length=100)
    is_deleted = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    verification_token = models.CharField(max_length=128, blank=True)
    from_google_auth = models.BooleanField(default=False)

    user_code = models.CharField(max_length=400, unique=True)
    bonus_money = models.PositiveBigIntegerField(default=0)

    def __str__(self):
        return self.get_full_name()

    @classmethod
    def generate_unique_string(cls):
        characters = string.ascii_letters + string.digits
        while True:
            value = ''.join(secrets.choice(characters) for _ in range(6))
            if not cls.objects.filter(user_code=value).exists():
                return value

    @property
    def is_active_user(self):
        return self.is_active and self.is_verified and not self.is_deleted

    @classmethod
    def user_id_exists(cls, user_code):
        return CustomUser.objects.filter(user_code=user_code, is_staff=False, is_active=True,
                                         is_verified=True, is_deleted=False).exists()

    def save(self, *args, **kwargs):
        self.first_name = normalize_text(self.first_name)
        self.last_name = normalize_text(self.last_name)

        if not self.pk:
            if self.is_staff:
                self.user_code = self.email
                self.is_verified = True
            else:
                self.user_code = CustomUser.generate_unique_string()

        self.bonus_money = round(self.bonus_money, 1)
        super().save(*args, **kwargs)

        CustomUser.objects.filter(date_joined__lt=now() - timedelta(minutes=30), is_verified=False).delete()
#
#
# class StudentCalledEmail(models.Model):
#     email = models.EmailField()
#     student = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
#     order = models.ForeignKey('payments.Order', on_delete=models.CASCADE, null=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#     bonus_added = models.BooleanField(default=False)
#
#     class Meta:
#         unique_together = ['student', 'email']
#
#     def save(self, *args, **kwargs):
#         order = self.order
#         if order and order.is_paid and not self.bonus_added:
#             try:
#                 called_student = CustomUser.objects.get(email=self.email)
#                 called_student.bonus_price += order.student_discount_price
#                 called_student.save()
#                 self.bonus_added = True
#             except CustomUser.DoesNotExist:
#                 pass
#         super().save(*args, **kwargs)
