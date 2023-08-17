from django.core.validators import MinValueValidator
from django.db import models


class TestBall(models.Model):
    ball = models.PositiveSmallIntegerField(validators=[MinValueValidator(1)])
