from django.db import models
from django.core.validators import MinValueValidator, FileExtensionValidator

from api.v1.general.services import normalize_text


class Chapter(models.Model):
    ordering_number = models.PositiveSmallIntegerField(primary_key=True, unique=True, verbose_name='ordering',
                                                       validators=[MinValueValidator(1)])
    image = models.ImageField(upload_to='chapters/images/', max_length=300,
                              validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'svg'])])

    lessons = models.PositiveSmallIntegerField(default=0)
    chapter_hour = models.PositiveSmallIntegerField(verbose_name='hour', default=0, editable=False)
    chapter_minute = models.PositiveSmallIntegerField(verbose_name='minute', default=0, editable=False)

    class Meta:
        verbose_name = 'Lesson Chapter'
        verbose_name_plural = 'Chapters'

    def __str__(self):
        return f'Chapter No {self.ordering_number}'


class ChapterDetail(models.Model):
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE)
    language = models.ForeignKey('languages.Language', on_delete=models.PROTECT)
    title = models.CharField(max_length=300)

    class Meta:
        unique_together = ['chapter', 'language']
        verbose_name = 'Chapter Language'
        verbose_name_plural = 'Chapter Languages'

    def __str__(self):
        return f'{self.language_id} Chapter No {self.chapter_id}'

    def save(self, *args, **kwargs):
        self.title = normalize_text(self.title)[0]
        super().save(*args, **kwargs)


class ChapterStudent(models.Model):
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE)
    student = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE)
    completed_lessons = models.PositiveSmallIntegerField(default=0)

    class Meta:
        unique_together = ['chapter', 'student']
