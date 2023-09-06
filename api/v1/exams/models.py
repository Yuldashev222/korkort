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

    created_at = models.DateTimeField(auto_now_add=True)
    time = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ['-id']

    def save(self, *args, **kwargs):
        if self.correct_answers > 0:
            self.percent = int(self.correct_answers / self.questions * 100) if self.questions > 0 else 0
        else:
            self.percent = 0
        super().save(*args, **kwargs)


class CategoryExamStudentResult(models.Model):
    category = models.ForeignKey('questions.QuestionCategory', on_delete=models.CASCADE)
    student = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE)
    percent = models.PositiveSmallIntegerField(default=0)
    exams = models.ManyToManyField(CategoryExamStudent)
