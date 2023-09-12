import string
import secrets

from django.db import models
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.password_validation import validate_password

from api.v1.balls.models import TestBall
from api.v1.general.services import normalize_text
from api.v1.accounts.managers import CustomUserManager


class CustomUser(AbstractUser):
    username = None
    REQUIRED_FIELDS = []
    USERNAME_FIELD = 'email'
    objects = CustomUserManager()

    email = models.EmailField(_("email address"), unique=True)
    password = models.CharField(_("password"), max_length=128, validators=[validate_password])
    first_name = models.CharField(_("name"), max_length=50)
    last_name = models.CharField(_("surname"), max_length=100)

    avatar_id = models.PositiveSmallIntegerField(blank=True, null=True)
    user_code = models.CharField(max_length=400, unique=True)
    bonus_money = models.FloatField(default=0)
    is_active = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False)

    google_id = models.CharField(max_length=100, default='-')
    facebook_id = models.CharField(max_length=100, default='-')

    level = models.PositiveSmallIntegerField(default=0)
    level_image_id = models.PositiveSmallIntegerField(default=0)

    ball = models.PositiveBigIntegerField(default=0)
    completed_lessons = models.PositiveSmallIntegerField(default=0)
    wrong_answers = models.PositiveIntegerField(default=0)
    last_exams_result = models.PositiveSmallIntegerField(default=0)

    tariff_expire_date = models.DateTimeField(default=now)

    class Meta:
        verbose_name = 'Student'
        verbose_name_plural = 'Students'
        ordering = ['-date_joined']

    def __str__(self):
        return self.get_full_name()[:30]

    @property
    def generate_unique_user_code(self):
        while True:
            value = ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(6))
            if not CustomUser.objects.filter(user_code=value).exists():
                return value

    @property
    def is_active_user(self):
        return self.is_active and self.is_verified

    @classmethod
    def user_id_exists(cls, user_code):
        return CustomUser.objects.filter(user_code=user_code, is_staff=False, is_active=True, is_verified=True).exists()

    def save(self, *args, **kwargs):
        self.ball = self.wrong_answers * TestBall.get_ball()
        self.first_name, self.last_name = normalize_text(self.first_name, self.last_name)
        self.bonus_money = round(self.bonus_money, 1)
        super().save(*args, **kwargs)
