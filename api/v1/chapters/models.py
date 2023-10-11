from django.db import models
from django.core.validators import MinValueValidator

from api.v1.general.services import normalize_text
from api.v1.chapters.services import chapter_image_location


class Chapter(models.Model):
    image = models.ImageField(upload_to=chapter_image_location, max_length=300)

    lessons = models.PositiveSmallIntegerField(default=0)
    ordering_number = models.PositiveSmallIntegerField(verbose_name='ordering', validators=[MinValueValidator(1)],
                                                       unique=True)
    chapter_hour = models.PositiveSmallIntegerField(default=0, editable=False)
    chapter_minute = models.PositiveSmallIntegerField(default=0, editable=False)

    class Meta:
        ordering = ['ordering_number']

    def __str__(self):
        return f'Chapter No {self.ordering_number}'


class ChapterDetail(models.Model):
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE)
    language = models.ForeignKey('languages.Language', on_delete=models.PROTECT)
    title = models.CharField(max_length=300)
    desc = models.CharField(max_length=700, blank=True)

    class Meta:
        unique_together = ['chapter', 'language']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.title, self.desc = normalize_text(self.title, self.desc)
        super().save(*args, **kwargs)


class ChapterStudent(models.Model):
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE)
    student = models.ForeignKey('accounts.CustomUser', on_delete=models.SET_NULL, null=True)
    completed_lessons = models.PositiveSmallIntegerField(default=0)

    def __str__(self):
        return str(self.chapter)

    class Meta:
        unique_together = ['chapter', 'student']
        ordering = ['chapter__ordering_number']
