from django.db import models
from django.core.exceptions import PermissionDenied
from django_ckeditor_5.fields import CKEditor5Field


class General(models.Model):
    privacy = CKEditor5Field()
    police = CKEditor5Field()

    def clean(self):
        if not self.pk and General.objects.exists():
            raise PermissionDenied("General can't be")
