from django.db import models
from django.core.cache import cache
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator


class TestBall(models.Model):
    ball = models.PositiveSmallIntegerField(validators=[MinValueValidator(1)])

    @classmethod
    def get_ball(cls):
        test_ball = cache.get('test_ball')
        if not test_ball:
            cls.set_redis()
            test_ball = cache.get('test_ball')
        return test_ball

    def clean(self):
        if not self.pk and TestBall.objects.exists():
            raise ValidationError('old ball object exists')

    def __str__(self):
        return str(self.ball)

    @classmethod
    def set_redis(cls):
        obj = cls.objects.first()
        if obj:
            cache.set('test_ball', obj.ball, 60 * 60 * 24 * 30)
        elif cache.get('test_ball'):
            cache.delete('test_ball')
