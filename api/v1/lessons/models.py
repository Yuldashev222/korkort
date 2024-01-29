import os

from django.conf import settings
from django.db import models
from django.core.cache import cache
from django.core.validators import MinValueValidator, FileExtensionValidator
from django_ckeditor_5.fields import CKEditor5Field

from api.v1.general.services import normalize_text
from api.v1.lessons.services import m3u8_zip_file_location


class Lesson(models.Model):
    image = models.ImageField(upload_to='lessons/images/',
                              validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'svg'])])

    chapter = models.ForeignKey('chapters.Chapter', on_delete=models.PROTECT)
    is_open = models.BooleanField(default=False)
    lesson_time = models.FloatField(help_text='in minute', validators=[MinValueValidator(1)])
    ordering_number = models.PositiveSmallIntegerField(validators=[MinValueValidator(1)])

    def __str__(self):
        return f'Chapter No {self.chapter_id} Lesson No {self.ordering_number}'

    class Meta:
        unique_together = ['chapter', 'ordering_number']

    @classmethod
    def get_all_lessons_count(cls):
        all_lessons_count = cache.get('all_lessons_count')
        if all_lessons_count is None:
            cls.set_redis()
            all_lessons_count = cache.get('all_lessons_count')
        return all_lessons_count

    @classmethod
    def set_redis(cls):
        cache.set('all_lessons_count', cls.objects.count())


class LessonDetail(models.Model):
    lesson = models.ForeignKey('lessons.Lesson', on_delete=models.CASCADE)
    language = models.ForeignKey('languages.Language', on_delete=models.PROTECT)
    title = models.CharField(max_length=300)
    short_title = models.CharField(max_length=200)

    m3u8_zip = models.FileField(max_length=300,
                                upload_to=m3u8_zip_file_location,
                                validators=[FileExtensionValidator(allowed_extensions=['zip'])],
                                null=True)  # delete on change

    text = CKEditor5Field(max_length=700, blank=True)

    def __str__(self):
        return f'{self.language_id} Lesson No {self.lesson}'

    class Meta:
        unique_together = ['lesson', 'language']

    def save(self, *args, **kwargs):
        self.title = normalize_text(self.title)[0]
        self.m3u8_url = self.m3u8_zip.url
        super().save(*args, **kwargs)

    def m3u8_url(self):
        list_dir = (f'chapters/{self.lesson.chapter_id}/lessons/{self.lesson_id}/'
                    f'videos/{self.language_id}/hls/')
        list_dir = 'chapters/1/lessons/191/videos/1/hls'  # last
        pwd_dir = os.path.join(settings.MEDIA_ROOT, list_dir)
        if not os.path.exists(pwd_dir):
            return ''
        for i in os.listdir(pwd_dir):
            if i.endswith('.m3u8'):
                return os.path.join(list_dir, i)
        return ''


class LessonWordInfo(models.Model):
    lesson_detail = models.ForeignKey(LessonDetail, on_delete=models.CASCADE)
    word = models.CharField(max_length=300)
    info = models.CharField(max_length=500)

    class Meta:
        verbose_name = 'Word Info'
        verbose_name_plural = 'Word Infos'

    def __str__(self):
        return self.word

    def save(self, *args, **kwargs):
        self.word, self.info = normalize_text(self.word, self.info)
        super().save(*args, **kwargs)


class LessonSource(models.Model):
    lesson_detail = models.ForeignKey(LessonDetail, on_delete=models.CASCADE)
    text = models.CharField(max_length=500)
    link = models.URLField()

    def save(self, *args, **kwargs):
        self.text = normalize_text(self.text)[0]
        super().save(*args, **kwargs)

    def __str__(self):
        return self.link

    class Meta:
        verbose_name = 'Source'
        verbose_name_plural = 'Sources'


class LessonStudent(models.Model):
    RATING = [(0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5)]
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    student = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE)

    is_completed = models.BooleanField(default=False)
    rating = models.PositiveSmallIntegerField(choices=RATING, default=RATING[0][0])

    class Meta:
        verbose_name = 'Student Lesson'
        verbose_name_plural = 'Student Lessons'
        unique_together = ['lesson', 'student']


class StudentLessonViewStatistics(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    student = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE)

    viewed_date = models.DateField()
