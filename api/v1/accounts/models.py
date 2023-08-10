import string
import secrets

from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.password_validation import validate_password

from api.v1.general.services import normalize_text

from .managers import CustomUserManager
from .tasks import delete_not_confirmed_accounts


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
    bonus_money = models.FloatField(default=0)

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

        delete_not_confirmed_accounts.delay()
