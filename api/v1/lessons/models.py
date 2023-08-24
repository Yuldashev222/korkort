from django.db import models
from ckeditor.fields import RichTextField
from django.core.cache import cache
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator


class Lesson(models.Model):
    chapter = models.ForeignKey('chapters.Chapter', on_delete=models.PROTECT)
    is_open = models.BooleanField(default=False)
    lesson_time = models.PositiveSmallIntegerField(validators=[MinValueValidator(1)], help_text='in minute')
    ordering_number = models.PositiveSmallIntegerField(default=1, validators=[MinValueValidator(1)], unique=True)
    image = models.ImageField(blank=True, null=True)

    title_swe = models.CharField(max_length=300, blank=True)
    title_en = models.CharField(max_length=300, blank=True)
    title_easy_swe = models.CharField(max_length=300, blank=True)

    text_swe = RichTextField(verbose_name='Swedish', blank=True, max_length=700)
    text_en = RichTextField(verbose_name='English', blank=True, max_length=700)
    text_easy_swe = RichTextField(verbose_name='Easy Swedish', blank=True, max_length=700)

    video_swe = models.FileField(blank=True, null=True, upload_to='lesson/videos')
    video_en = models.FileField(blank=True, null=True, upload_to='lesson/videos')
    video_easy_swe = models.FileField(blank=True, null=True, upload_to='lesson/videos')

    created_at = models.DateTimeField(auto_now_add=True)

    @classmethod
    def set_redis(cls):
        cnt = cls.objects.count()
        cache.set('all_lesson_count', cnt, 60 * 60 * 24 * 7)

    def clean(self):
        if not (self.title_en or self.title_swe or self.title_easy_swe):
            raise ValidationError('Enter the title')

        if not (self.text_en or self.text_swe or self.text_easy_swe or self.video_en or self.video_swe or
                self.video_easy_swe):
            raise ValidationError('Enter the text or video')

    def save(self, *args, **kwargs):
        self.title_en = ' '.join(self.title_en.split())
        self.title_swe = ' '.join(self.title_swe.split())
        self.title_easy_swe = ' '.join(self.title_easy_swe.split())
        super().save(*args, **kwargs)


class LessonWordInfo(models.Model):
    text_swe = models.CharField(max_length=300)
    text_en = models.CharField(max_length=300)
    text_easy_swe = models.CharField(max_length=300)
    info_swe = models.TextField(max_length=500)
    info_en = models.TextField(max_length=500)
    info_easy_swe = models.TextField(max_length=500)

    lessons = models.ManyToManyField(Lesson)

    def save(self, *args, **kwargs):
        self.text = ' '.join(self.text_swe.split())
        self.text = ' '.join(self.text_en.split())
        self.text = ' '.join(self.text_easy_swe.split())
        self.info = ' '.join(self.info_swe.split())
        self.info = ' '.join(self.info_en.split())
        self.info = ' '.join(self.info_easy_swe.split())
        super().save(*args, **kwargs)


class LessonSource(models.Model):
    text_swe = models.TextField(max_length=500)
    text_en = models.TextField(max_length=500)
    text_easy_swe = models.TextField(max_length=500)
    link = models.URLField()

    lessons = models.ManyToManyField(Lesson)

    def save(self, *args, **kwargs):
        self.text = ' '.join(self.text_swe.split())
        self.text = ' '.join(self.text_en.split())
        self.text = ' '.join(self.text_easy_swe.split())
        super().save(*args, **kwargs)


class LessonStudent(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    student = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE)

    is_completed = models.BooleanField(default=False)
    ball = models.PositiveSmallIntegerField(default=0)

    class Meta:
        unique_together = ['lesson', 'student']


class LessonStudentStatistics(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.SET_NULL, null=True)
    student = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE)

    viewed_date = models.DateField(auto_now_add=True)

    class Meta:
        unique_together = ['lesson', 'student']


class LessonStudentStatisticsByDay(models.Model):
    count = models.PositiveIntegerField(default=0)
    date = models.DateField(unique=True)
    student = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE)
