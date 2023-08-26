from django.db import models
from django.core.cache import cache
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator


class TestBall(models.Model):  # last | on change
    ball = models.PositiveSmallIntegerField(validators=[MinValueValidator(1)])

    def clean(self):
        if not self.pk and TestBall.objects.exists():
            raise ValidationError('old ball object exists')

    def __str__(self):
        return str(self.ball)

    @classmethod
    def set_redis(cls):
        obj = cls.objects.first()
        if obj:
            cache.set('test_ball', obj.ball, 60 * 60 * 24 * 7)
        elif cache.get('student_discount'):
            cache.delete('student_discount')
