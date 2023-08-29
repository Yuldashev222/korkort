from django.db import models
from ckeditor.fields import RichTextField
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator

from api.v1.lessons.models import LessonStudent
from api.v1.accounts.models import CustomUser


class Chapter(models.Model):
    title_swe = models.CharField(max_length=300, blank=True)
    title_en = models.CharField(max_length=300, blank=True)
    title_e_swe = models.CharField(max_length=300, blank=True)

    desc_swe = RichTextField(verbose_name='Swedish', blank=True, max_length=700)
    desc_en = RichTextField(verbose_name='English', blank=True, max_length=700)
    desc_e_swe = RichTextField(verbose_name='Easy Swedish', blank=True, max_length=700)

    image = models.ImageField(blank=True, null=True)

    lessons = models.PositiveSmallIntegerField(default=0)
    ordering_number = models.PositiveSmallIntegerField(default=1, validators=[MinValueValidator(1)], unique=True)
    chapter_hour = models.PositiveSmallIntegerField(default=0, editable=False)
    chapter_minute = models.PositiveSmallIntegerField(default=0, editable=False)

    def save(self, *args, **kwargs):
        created = True if not self.pk else False
        super().save(*args, **kwargs)
        if created:
            students = CustomUser.objects.filter(is_staff=False)
            objs = [ChapterStudent(student=student, chapter=self) for student in students]
            ChapterStudent.objects.bulk_create(objs)

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

    def save(self, *args, **kwargs):
        obj = LessonStudent.objects.filter(student=self.student, lesson__chapter=self.chapter, is_completed=True
                                           ).order_by('lesson__ordering_number').last()
        if not obj:
            obj = LessonStudent.objects.filter(student=self.student, lesson__chapter=self.chapter
                                               ).order_by('lesson__ordering_number').first()
        self.last_lesson = obj if obj else None
        super().save(*args, **kwargs)
