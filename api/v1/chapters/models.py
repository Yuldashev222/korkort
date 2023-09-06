from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator


class Chapter(models.Model):
    title_swe = models.CharField(max_length=300, blank=True)
    title_en = models.CharField(max_length=300, blank=True)
    title_e_swe = models.CharField(max_length=300, blank=True)

    desc_swe = models.CharField(verbose_name='Swedish', blank=True, max_length=700)
    desc_en = models.CharField(verbose_name='English', blank=True, max_length=700)
    desc_e_swe = models.CharField(verbose_name='Easy Swedish', blank=True, max_length=700)

    image = models.ImageField(blank=True, null=True)

    lessons = models.PositiveSmallIntegerField(default=0)
    ordering_number = models.PositiveSmallIntegerField(default=1, validators=[MinValueValidator(1)], unique=True)
    chapter_hour = models.PositiveSmallIntegerField(default=0, editable=False)
    chapter_minute = models.PositiveSmallIntegerField(default=0, editable=False)

    class Meta:
        ordering = ['ordering_number']

    def __str__(self):
        return f'Chapter No {self.ordering_number}'

    def clean(self):
        if not (self.title_en or self.title_swe or self.title_e_swe):
            raise ValidationError('Enter the title')


class ChapterStudent(models.Model):
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE)
    student = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE)
    completed_lessons = models.PositiveSmallIntegerField(default=0)
    last_lesson = models.ForeignKey('lessons.LessonStudent', on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        unique_together = ['chapter', 'student']
        ordering = ['chapter__ordering_number']
