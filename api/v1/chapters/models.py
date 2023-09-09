from django.db import models
from django.core.validators import MinValueValidator

from api.v1.chapters.services import chapter_image_location


class Chapter(models.Model):
    title_en = models.CharField(verbose_name='title English', max_length=300, blank=True)
    title_swe = models.CharField(verbose_name='title Swedish', max_length=300)
    title_e_swe = models.CharField(verbose_name='title Easy Swedish', max_length=300, blank=True)

    desc_en = models.CharField(verbose_name='desc English', blank=True, max_length=700)
    desc_swe = models.CharField(verbose_name='desc Swedish', blank=True, max_length=700)
    desc_e_swe = models.CharField(verbose_name='desc Easy Swedish', blank=True, max_length=700)

    image = models.ImageField(upload_to=chapter_image_location, max_length=300)

    lessons = models.PositiveSmallIntegerField(default=0)
    ordering_number = models.PositiveSmallIntegerField(verbose_name='ordering',
                                                       default=1, validators=[MinValueValidator(1)], unique=True)
    chapter_hour = models.PositiveSmallIntegerField(default=0, editable=False)
    chapter_minute = models.PositiveSmallIntegerField(default=0, editable=False)

    class Meta:
        ordering = ['ordering_number']

    def __str__(self):
        return f'{self.ordering_number}: {self.title_swe}'[:30]


class ChapterStudent(models.Model):
    chapter = models.ForeignKey(Chapter, on_delete=models.SET_NULL, null=True)
    student = models.ForeignKey('accounts.CustomUser', on_delete=models.SET_NULL, null=True)
    completed_lessons = models.PositiveSmallIntegerField(default=0)
    last_lesson = models.ForeignKey('lessons.LessonStudent', on_delete=models.SET_NULL, null=True, blank=True)
    is_open = models.BooleanField(default=False)

    def __str__(self):
        return str(self.chapter)

    class Meta:
        unique_together = ['chapter', 'student']
        ordering = ['chapter__ordering_number']
