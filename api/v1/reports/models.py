from django.db import models

from config import settings


class Report(models.Model):
    student = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE)
    lesson = models.ForeignKey('lessons.Lesson', on_delete=models.CASCADE, null=True)
    question = models.ForeignKey('questions.Question', on_delete=models.CASCADE, null=True)
    report_type = models.IntegerField(choices=settings.REPORT_TYPES)
    desc = models.CharField(max_length=500, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_completed = models.BooleanField(default=False)
