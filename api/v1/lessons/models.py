from django.db import models
from django.core.cache import cache
from django.core.validators import MinValueValidator, FileExtensionValidator

from api.v1.general.services import normalize_text
from api.v1.lessons.services import lesson_image_location, lesson_video_location


class Lesson(models.Model):
    image = models.ImageField(upload_to=lesson_image_location)
    chapter = models.ForeignKey('chapters.Chapter', on_delete=models.PROTECT)
    is_open = models.BooleanField(default=False)
    lesson_time = models.FloatField(help_text='in minute')
    ordering_number = models.PositiveSmallIntegerField(default=1, validators=[MinValueValidator(1)])

    title_en = models.CharField(verbose_name='Title English', max_length=300, blank=True)
    title_swe = models.CharField(verbose_name='Title Swedish', max_length=300)
    title_e_swe = models.CharField(verbose_name='Title Easy Swedish', max_length=300, blank=True)

    text_en = models.CharField(verbose_name='Text English', blank=True, max_length=700)
    text_swe = models.CharField(verbose_name='Text Swedish', blank=True, max_length=700)
    text_e_swe = models.CharField(verbose_name='Text Easy Swedish', blank=True, max_length=700)

    video_en = models.FileField(blank=True, null=True, upload_to=lesson_video_location, max_length=300,
                                validators=[FileExtensionValidator(allowed_extensions=['mp4'])])
    video_swe = models.FileField(upload_to=lesson_video_location, max_length=300,
                                 validators=[FileExtensionValidator(allowed_extensions=['mp4'])])
    video_e_swe = models.FileField(blank=True, null=True, upload_to=lesson_video_location, max_length=300,
                                   validators=[FileExtensionValidator(allowed_extensions=['mp4'])])

    def __str__(self):
        return f'{self.ordering_number}: {self.title_swe}'[:30]

    class Meta:
        ordering = ['ordering_number']
        unique_together = ['chapter', 'ordering_number']

    @classmethod
    def set_redis(cls):
        cnt = cls.objects.count()
        last_open_lesson = cls.objects.filter(is_open=True).last()
        if last_open_lesson:
            cache.set('last_open_lesson_id', last_open_lesson.id, 60 * 60 * 24 * 30)
        elif cache.get('last_open_lesson_id'):
            cache.delete('last_open_lesson_id')
        cache.set('all_lessons_count', cnt, 60 * 60 * 24 * 30)

    def save(self, *args, **kwargs):
        # self.lesson_time = get_video_duration(self.video_swe.path)
        self.title_swe, self.title_en, self.title_e_swe = normalize_text(self.title_swe,
                                                                         self.title_en, self.title_e_swe)
        super().save(*args, **kwargs)


class LessonWordInfo(models.Model):
    text_swe = models.CharField(max_length=300)
    text_en = models.CharField(max_length=300, blank=True)
    text_e_swe = models.CharField(max_length=300, blank=True)

    info_swe = models.CharField(max_length=500)
    info_en = models.CharField(max_length=500, blank=True)
    info_e_swe = models.CharField(max_length=500, blank=True)

    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)  # last

    class Meta:
        verbose_name = 'Word Info'
        verbose_name_plural = 'Word Infos'

    def save(self, *args, **kwargs):
        self.text_swe, self.text_en, self.text_e_swe, self.info_swe, self.info_en, self.info_e_swe = normalize_text(
            self.text_swe, self.text_en, self.text_e_swe, self.info_swe, self.info_en, self.info_e_swe)
        super().save(*args, **kwargs)


class LessonSource(models.Model):
    text_swe = models.CharField(max_length=500)
    text_en = models.CharField(max_length=500, blank=True)
    text_e_swe = models.CharField(max_length=500, blank=True)

    link = models.URLField()

    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        self.text_swe, self.text_en, self.text_e_swe = normalize_text(self.text_swe, self.text_en, self.text_e_swe)
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
