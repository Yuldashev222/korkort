from django.db import models
from django.conf import settings
from django.utils import timezone
from rest_framework.authtoken.models import Token


class CustomToken(Token):
    expires_at = models.DateTimeField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.expires_at:
            self.expires_at = timezone.now() + timezone.timedelta(days=settings.TOKEN_EXPIRE_DAY)
        super().save(*args, **kwargs)
