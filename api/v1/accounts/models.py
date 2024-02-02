import string
import secrets
from django.db import models
from django.core.validators import MaxValueValidator
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.contrib.auth.password_validation import validate_password

from api.v1.accounts.managers import CustomUserManager


class CustomUser(AbstractUser):
    username = None
    first_name = None
    last_name = None
    REQUIRED_FIELDS = []
    USERNAME_FIELD = 'email'
    objects = CustomUserManager()

    email = models.EmailField(_("email address"), unique=True)
    password = models.CharField(_("password"), max_length=128, validators=[validate_password])
    name = models.CharField(_("name"), max_length=100)

    avatar_id = models.PositiveSmallIntegerField(default=0, validators=[MaxValueValidator(500)])
    user_code = models.CharField(max_length=400, unique=True)
    bonus_money = models.FloatField(default=0)
    is_active = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False)
    level_id = models.PositiveSmallIntegerField(default=1)
    level_percent = models.PositiveSmallIntegerField(default=0)
    auth_provider = models.CharField(max_length=100, default='backend')

    completed_lessons = models.PositiveSmallIntegerField(default=0)
    correct_answers = models.PositiveIntegerField(default=0)
    ball = models.PositiveIntegerField(default=0)

    tariff_expire_date = models.DateField()

    class Meta:
        verbose_name = 'Student'
        verbose_name_plural = 'Students'

    def __str__(self):
        return self.name

    @property
    def generate_unique_user_code(self):
        while True:
            value = ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(6))
            if not CustomUser.objects.filter(user_code=value).exists():
                return value

    @property
    def is_active_user(self):
        return self.is_active  # and self.is_verified

    @classmethod
    def user_code_exists(cls, user_code):
        return CustomUser.objects.filter(user_code=user_code, is_staff=False,  # is_verified=True,
                                         is_active=True).exists()
