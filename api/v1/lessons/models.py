from ckeditor.fields import RichTextField
from django.db import models
from django.core.cache import cache
from django.core.validators import MinValueValidator, FileExtensionValidator

from api.v1.general.services import normalize_text


class Lesson(models.Model):
    image = models.ImageField(upload_to='lessons/images/')
    chapter = models.ForeignKey('chapters.Chapter', on_delete=models.PROTECT)
    is_open = models.BooleanField(default=False)
    lesson_time = models.FloatField(help_text='in minute')
    ordering_number = models.PositiveSmallIntegerField(validators=[MinValueValidator(1)])

    def __str__(self):
        return f'{self.chapter}: Lesson No {self.ordering_number}'

    class Meta:
        ordering = ['ordering_number']
        unique_together = ['chapter', 'ordering_number']

    @classmethod
    def get_all_lessons_count(cls):
        all_lessons_count = cache.get('all_lessons_count')
        if not all_lessons_count:
            cls.set_redis()
            all_lessons_count = cache.get('all_lessons_count')
        return all_lessons_count

    @classmethod
    def set_redis(cls):
        cache.set('all_lessons_count', cls.objects.count())


class LessonDetail(models.Model):
    lesson = models.ForeignKey('lessons.Lesson', on_delete=models.CASCADE)
    language = models.ForeignKey('languages.Language', on_delete=models.PROTECT)
    text = RichTextField(max_length=700, blank=True)
    video = models.FileField(max_length=300, upload_to='lessons/videos/',
                             validators=[FileExtensionValidator(allowed_extensions=['mp4'])])
    title = models.CharField(max_length=300)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['lesson__ordering_number']
        unique_together = ['lesson', 'language']

    def save(self, *args, **kwargs):
        self.title = normalize_text(self.title)[0]
        super().save(*args, **kwargs)


class LessonWordInfo(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    language = models.ForeignKey('languages.Language', on_delete=models.PROTECT)
    word = models.CharField(max_length=300)
    info = models.CharField(max_length=500)

    class Meta:
        verbose_name = 'Word Info'
        verbose_name_plural = 'Word Infos'

    def save(self, *args, **kwargs):
        self.word, self.info = normalize_text(self.word, self.info)
        super().save(*args, **kwargs)


class LessonSource(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    language = models.ForeignKey('languages.Language', on_delete=models.PROTECT)
    text = models.CharField(max_length=500)
    link = models.URLField()

    def save(self, *args, **kwargs):
        self.text = normalize_text(self.text)[0]
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Source'
        verbose_name_plural = 'Sources'


class LessonStudent(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    student = models.ForeignKey('accounts.CustomUser', on_delete=models.SET_NULL, null=True)

    is_completed = models.BooleanField(default=False)
    ball = models.PositiveSmallIntegerField(default=0)

    class Meta:
        verbose_name = 'Student Lesson'
        verbose_name_plural = 'Student Lessons'
        unique_together = ['lesson', 'student']
        ordering = ['lesson__ordering_number']


class StudentLessonViewStatistics(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.SET_NULL, null=True)
    student = models.ForeignKey('accounts.CustomUser', on_delete=models.SET_NULL, null=True)

    viewed_date = models.DateField()

    class Meta:
        ordering = ['-viewed_date']
