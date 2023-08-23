from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator


class QuestionCategory(models.Model):
    name = models.CharField(max_length=300)

    def __str__(self):
        return self.name


class QuestionAbstractMixin(models.Model):
    DIFFICULTY_LEVEL = [
        [1, 'easy'],
        [2, 'normal'],
        [3, 'hard']
    ]
    difficulty_level = models.PositiveSmallIntegerField(choices=DIFFICULTY_LEVEL, default=DIFFICULTY_LEVEL[0][0])
    category = models.ForeignKey(QuestionCategory, on_delete=models.PROTECT, null=True)  # last

    text_swe = models.CharField(max_length=300, verbose_name='Swedish', blank=True)
    text_en = models.CharField(max_length=300, verbose_name='English', blank=True)
    text_easy_swe = models.CharField(max_length=300, verbose_name='Easy Swedish', blank=True)

    video_swe = models.FileField(blank=True, null=True)
    video_eng = models.FileField(blank=True, null=True)
    video_easy_swe = models.FileField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True, null=True)
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

    class Meta:
        abstract = True


class VariantAbstractMixin(models.Model):
    is_correct = models.BooleanField(default=False)

    text_swe = models.CharField(max_length=300, verbose_name='Swedish', blank=True)
    text_en = models.CharField(max_length=300, verbose_name='English', blank=True)
    text_easy_swe = models.CharField(max_length=300, verbose_name='Easy Swedish', blank=True)

    created_at = models.DateTimeField(auto_now_add=True, null=True)  # last

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


class ExamQuestion(QuestionAbstractMixin):
    chapter = models.ForeignKey('chapters.Chapter', on_delete=models.PROTECT)


class LessonQuestion(QuestionAbstractMixin):
    lesson = models.ForeignKey('lessons.Lesson', on_delete=models.SET_NULL, null=True)
    ordering_number = models.PositiveSmallIntegerField(default=1, validators=[MinValueValidator(1)], unique=True)


class ExamVariant(VariantAbstractMixin):
    question = models.ForeignKey(ExamQuestion, on_delete=models.CASCADE)

    def clean(self):
        if self.is_correct and ExamVariant.objects.exclude(pk=self.pk).filter(question=self.question,
                                                                              is_correct=True).exists():
            raise ValidationError('there must be only one correct answer!')
        super().clean()


class LessonVariant(VariantAbstractMixin):
    question = models.ForeignKey(LessonQuestion, on_delete=models.CASCADE)

    def clean(self):
        if self.is_correct and LessonVariant.objects.exclude(pk=self.pk).filter(lesson_question=self.question,
                                                                                is_correct=True).exists():
            raise ValidationError('there must be only one correct answer!')
        super().clean()


class WrongQuestionStudent(models.Model):
    question = models.ForeignKey(ExamQuestion, on_delete=models.CASCADE)
    student = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.question}'


class SavedQuestionStudent(models.Model):
    question = models.ForeignKey(ExamQuestion, on_delete=models.CASCADE)
    student = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.question}'
