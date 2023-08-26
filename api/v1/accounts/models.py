import string
import secrets

from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.password_validation import validate_password

from api.v1.levels.models import Level
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

    avatar_id = models.PositiveSmallIntegerField(blank=True, null=True)
    user_code = models.CharField(max_length=400, unique=True)
    bonus_money = models.FloatField(default=0)

    is_deleted = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)

    google_id = models.CharField(max_length=100, blank=True)
    facebook_id = models.CharField(max_length=100, blank=True)

    level = models.ForeignKey('levels.Level', on_delete=models.PROTECT, null=True)
    level_image_id = models.PositiveSmallIntegerField(default=0)

    ball = models.PositiveBigIntegerField(default=0)
    completed_lessons = models.PositiveSmallIntegerField(default=0)
    correct_answers = models.PositiveIntegerField(default=0)
    last_exams_result = models.PositiveSmallIntegerField(default=0)

    tariff_expire_date = models.DateTimeField(null=True)

    def __str__(self):
        return self.get_full_name()

    @property
    def generate_unique_user_code(self):
        while True:
            value = ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(6))
            if not CustomUser.objects.filter(user_code=value).exists():
                return value

    @property
    def is_active_user(self):
        return self.is_active and self.is_verified and not self.is_deleted

    @classmethod
    def user_id_exists(cls, user_code):
        return CustomUser.objects.filter(user_code=user_code, is_staff=False, is_active=True,
                                         is_verified=True, is_deleted=False).exists()

    def save(self, *args, **kwargs):
        self.first_name, self.last_name = normalize_text(self.first_name, self.last_name)
        self.bonus_money = round(self.bonus_money, 1)

        if not self.pk:
            if self.is_staff:
                self.user_code = self.email
                self.is_verified = True
            else:
                self.user_code = self.generate_unique_user_code
                self.level, _ = Level.objects.get_or_create(level=1, title='beginner')

        super().save(*args, **kwargs)
