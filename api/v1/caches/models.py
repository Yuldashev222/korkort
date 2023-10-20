from django.db import models
from django.core.cache import cache


class SetCache(models.Model):
    clear_cache = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Clear Cache'
        verbose_name_plural = 'Caches'

    def save(self, *args, **kwargs):
        if self.clear_cache:
            cache.clear()
            self.clear_cache = False
        super().save(*args, **kwargs)
