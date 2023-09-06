from django.db import models
from django.conf import settings
from django.core.validators import MaxValueValidator

from api.v1.questions.models import Question


class CategoryExamStudent(models.Model):
    student = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE)
    category = models.ForeignKey('questions.QuestionCategory', on_delete=models.PROTECT)
    correct_answers = models.PositiveSmallIntegerField(default=0)
    difficulty_level = models.PositiveSmallIntegerField(choices=Question.DIFFICULTY_LEVEL, null=True)

    # last
    questions = models.PositiveSmallIntegerField(default=0, validators=[MaxValueValidator(settings.MAX_QUESTIONS)])
    percent = models.PositiveSmallIntegerField(default=0)

    created_at = models.DateTimeField(auto_now=True)
    time = models.PositiveSmallIntegerField(default=0)

    def save(self, *args, **kwargs):
        self.percent = int(self.correct_answers / self.questions * 100) if self.questions > 0 else 0
        super().save(*args, **kwargs)
