from ckeditor.fields import RichTextField
from django.core.exceptions import ValidationError
from django.db import models


class Chapter(models.Model):
    title_swe = models.CharField(max_length=300, blank=True)
    title_en = models.CharField(max_length=300, blank=True)
    title_easy_swe = models.CharField(max_length=300, blank=True)

    desc_swe = RichTextField(verbose_name='Swedish', blank=True)
    desc_en = RichTextField(verbose_name='English', blank=True)
    desc_easy_swe = RichTextField(verbose_name='Easy Swedish', blank=True)

    image = models.ImageField(blank=True, null=True)

    chapter_hour = models.PositiveSmallIntegerField(default=0, editable=False)
    chapter_minute = models.PositiveSmallIntegerField(default=0, editable=False)

    def clean(self):
        if not (self.title_en or self.title_swe or self.title_easy_swe):
            raise ValidationError('Enter the title')
