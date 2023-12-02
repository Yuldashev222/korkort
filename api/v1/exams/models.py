from django.db import models
from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator

from api.v1.questions.models import Question


class CategoryExamStudent(models.Model):
    category = models.ForeignKey('questions.Category', on_delete=models.CASCADE)
    student = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE)
    correct_answers = models.PositiveSmallIntegerField(default=0)
    questions = models.PositiveSmallIntegerField(validators=[MaxValueValidator(settings.MAX_QUESTIONS),
                                                             MinValueValidator(settings.MIN_QUESTIONS)])
    percent = models.PositiveSmallIntegerField(default=0)

    def save(self, *args, **kwargs):
        if self.correct_answers > 0 and self.questions > 0:
            self.percent = int(self.correct_answers / self.questions * 100)
        else:
            self.percent = 0
        super().save(*args, **kwargs)


class StudentLastExamResult(models.Model):
    student = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE)
    questions = models.PositiveSmallIntegerField(validators=[MinValueValidator(1)])
    wrong_answers = models.PositiveSmallIntegerField()


class FinalExamStudent(models.Model):
    questions = models.PositiveSmallIntegerField()
    correct_answers = models.PositiveSmallIntegerField()
    student = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE)
    percent = models.PositiveSmallIntegerField(default=0)

    def save(self, *args, **kwargs):
        if self.correct_answers > 0 and self.questions > 0:
            self.percent = int(self.correct_answers / self.questions * 100)
        else:
            self.percent = 0
        super().save(*args, **kwargs)
