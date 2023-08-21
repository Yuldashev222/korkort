from django.db import models
from ckeditor.fields import RichTextField
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator


class Lesson(models.Model):
    chapter = models.ForeignKey('chapters.Chapter', on_delete=models.PROTECT)
    is_open = models.BooleanField(default=False)
    lesson_time = models.PositiveSmallIntegerField(validators=[MinValueValidator(1)], help_text='in minute')
    ordering_number = models.PositiveSmallIntegerField(default=1, validators=[MinValueValidator(1)])
    image = models.ImageField(blank=True, null=True)

    title_swe = models.CharField(max_length=300, blank=True)
    title_en = models.CharField(max_length=300, blank=True)
    title_easy_swe = models.CharField(max_length=300, blank=True)

    text_swe = RichTextField(verbose_name='Swedish', blank=True)
    text_en = RichTextField(verbose_name='English', blank=True)
    text_easy_swe = RichTextField(verbose_name='Easy Swedish', blank=True)

    video_swe = models.FileField(blank=True, null=True)
    video_en = models.FileField(blank=True, null=True)
    video_easy_swe = models.FileField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        if not (self.title_en or self.title_swe or self.title_easy_swe):
            raise ValidationError('Enter the title')

        if not (self.text_en or self.text_swe or self.text_easy_swe or self.video_en or self.video_swe or
                self.video_easy_swe):
            raise ValidationError('Enter the text or video')

    def save(self, *args, **kwargs):
        self.title_swe = ' '.join(self.title_swe.split())
        self.title_en = ' '.join(self.title_en.split())
        self.title_easy_swe = ' '.join(self.title_easy_swe.split())
        super().save(*args, **kwargs)


class LessonWordInfo(models.Model):
    text = models.CharField(max_length=300)
    info = models.TextField(max_length=500)

    lesson = models.ManyToManyField(Lesson)

    def save(self, *args, **kwargs):
        self.text = ' '.join(self.text.split())
        self.info = ' '.join(self.info.split())
        super().save(*args, **kwargs)


class LessonSource(models.Model):
    text = models.TextField(max_length=500)
    link = models.URLField()

    lesson = models.ManyToManyField(Lesson)

    def save(self, *args, **kwargs):
        self.text = ' '.join(self.text.split())
        super().save(*args, **kwargs)


class LessonStudent(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    student = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE)

    is_completed = models.BooleanField(default=False)
    ball = models.PositiveSmallIntegerField(default=0)

    class Meta:
        unique_together = ['lesson', 'student']
