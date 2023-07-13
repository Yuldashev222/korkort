from datetime import timedelta

from django.contrib.auth.password_validation import validate_password
from django.db import models
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser

from .managers import CustomUserManager
from api.v1.general.services import normalize_text


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

    def __str__(self):
        return self.get_full_name()

    @property
    def is_active_user(self):
        return self.is_active and self.is_verified and not self.is_deleted

    def save(self, *args, **kwargs):
        self.first_name = normalize_text(self.first_name)
        self.last_name = normalize_text(self.last_name)
        if self.is_staff:
            self.is_verified = True
        super().save(*args, **kwargs)

        CustomUser.objects.filter(date_joined__lt=now() - timedelta(minutes=30), is_verified=False).delete()
