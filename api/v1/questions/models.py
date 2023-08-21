from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator


class QuestionCategory(models.Model):
    chapter = models.ForeignKey('chapters.Chapter', on_delete=models.PROTECT)
    name = models.CharField(max_length=300)

    def __str__(self):
        return self.name


class Question(models.Model):
    DIFFICULTY_LEVEL = [
        ['easy', 1],
        ['average', 2],
        ['difficult', 3]
    ]
    difficulty_level = models.PositiveSmallIntegerField(choices=DIFFICULTY_LEVEL, default=DIFFICULTY_LEVEL[0][1])
    category = models.ForeignKey(QuestionCategory, on_delete=models.PROTECT)

    text_swe = models.CharField(max_length=300, verbose_name='Swedish', blank=True)
    text_en = models.CharField(max_length=300, verbose_name='English', blank=True)
    text_easy_swe = models.CharField(max_length=300, verbose_name='Easy Swedish', blank=True)

    video_swe = models.FileField(blank=True, null=True)
    video_eng = models.FileField(blank=True, null=True)
    video_easy_swe = models.FileField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        text = self.text_swe or self.text_easy_swe or self.text_en
        return f'{self.id}::{text}'

    def save(self, *args, **kwargs):
        self.text_swe = ' '.join(self.text_swe.split())
        self.text_en = ' '.join(self.text_en.split())
        self.text_easy_swe = ' '.join(self.text_easy_swe.split())
        super().save(*args, **kwargs)

    def clean(self):
        if not (self.text_en or self.text_swe or self.text_easy_swe):
            raise ValidationError('Enter the text')


class Variant(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    is_correct = models.BooleanField(default=False)

    text_swe = models.CharField(max_length=300, verbose_name='Swedish', blank=True)
    text_en = models.CharField(max_length=300, verbose_name='English', blank=True)
    text_easy_swe = models.CharField(max_length=300, verbose_name='Easy Swedish', blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        text = self.text_swe or self.text_easy_swe or self.text_en
        return f'{self.id}::{text}'

    def save(self, *args, **kwargs):
        self.text_swe = ' '.join(self.text_swe.split())
        self.text_en = ' '.join(self.text_en.split())
        self.text_easy_swe = ' '.join(self.text_easy_swe.split())
        super().save(*args, **kwargs)

    def clean(self):
        if self.is_correct and Variant.objects.exclude(pk=self.pk).filter(question=self.question,
                                                                          is_correct=True).exists():
            raise ValidationError('there must be only one correct answer!')

        if not (self.text_en or self.text_swe or self.text_easy_swe):
            raise ValidationError('Enter the text')


class WrongQuestionStudent(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    student = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.question}'


class SavedQuestionStudent(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    student = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.question}'
