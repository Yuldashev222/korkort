from django.db import models
from django.core.cache import cache
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator

from api.v1.accounts.models import CustomUser
from api.v1.general.services import normalize_text
from api.v1.questions.services import category_image_location, question_image_location, question_video_location


class QuestionCategory(models.Model):
    name_swe = models.CharField(max_length=300)
    name_en = models.CharField(max_length=300, blank=True)
    name_e_swe = models.CharField(max_length=300, blank=True)
    image = models.ImageField(upload_to=category_image_location, max_length=300)

    def __str__(self):
        return self.name_swe[:30]


class Question(models.Model):
    DIFFICULTY_LEVEL = [
        [1, 'easy'],
        [2, 'normal'],
        [3, 'hard']
    ]
    lesson = models.ForeignKey('lessons.Lesson', on_delete=models.PROTECT)
    category = models.ForeignKey(QuestionCategory, on_delete=models.PROTECT)
    for_lesson = models.BooleanField(default=False)
    ordering_number = models.PositiveSmallIntegerField(validators=[MinValueValidator(1)], null=True)
    difficulty_level = models.PositiveSmallIntegerField(choices=DIFFICULTY_LEVEL, default=DIFFICULTY_LEVEL[0][0])

    answer = models.CharField(max_length=500, blank=True)

    text_swe = models.CharField(max_length=300, verbose_name='Swedish')
    text_en = models.CharField(max_length=300, verbose_name='English', blank=True)
    text_e_swe = models.CharField(max_length=300, verbose_name='Easy Swedish', blank=True)

    video_swe = models.FileField(upload_to=question_video_location, blank=True, null=True, max_length=300)
    video_en = models.FileField(upload_to=question_video_location, blank=True, null=True, max_length=300)
    video_e_swe = models.FileField(upload_to=question_video_location, blank=True, null=True, max_length=300)
    
    image_swe = models.ImageField(upload_to=question_image_location, blank=True, null=True, max_length=300)
    image_en = models.ImageField(upload_to=question_image_location, blank=True, null=True, max_length=300)
    image_e_swe = models.ImageField(upload_to=question_image_location, blank=True, null=True, max_length=300)

    def __str__(self):
        return f'{self.id}: {self.text_swe}'[:30]

    class Meta:
        ordering = ['ordering_number']
        unique_together = ['lesson', 'for_lesson', 'ordering_number']

    def save(self, *args, **kwargs):
        self.text_swe, self.text_en, self.text_e_swe, self.answer = normalize_text(self.text_swe, self.text_en,
                                                                                   self.text_e_swe, self.answer)
        super().save(*args, **kwargs)

    def clean(self):
        if not (self.text_en or self.text_swe or self.text_e_swe):
            raise ValidationError('Enter the text')

    @classmethod
    def set_redis(cls):
        cnt = Question.objects.count()
        cache.set('all_questions_count', cnt, 60 * 60 * 24 * 7)


class Variant(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)

    is_correct = models.BooleanField(default=False)

    text_swe = models.CharField(max_length=300, verbose_name='Swedish')
    text_en = models.CharField(max_length=300, verbose_name='English', blank=True)
    text_e_swe = models.CharField(max_length=300, verbose_name='Easy Swedish', blank=True)

    def save(self, *args, **kwargs):
        self.text_swe, self.text_en, self.text_e_swe = normalize_text(self.text_swe, self.text_en, self.text_e_swe)
        super().save(*args, **kwargs)

    def clean(self):
        if not (self.text_en or self.text_swe or self.text_e_swe):
            raise ValidationError('Enter the text')


class StudentWrongAnswer(models.Model):
    student = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.question)


class StudentSavedQuestion(models.Model):
    student = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.question)

    class Meta:
        ordering = ['-created_at']
        unique_together = ['question', 'student']


class QuestionStudentLastResult(models.Model):
    student = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE)
    questions = models.PositiveSmallIntegerField()
    wrong_answers = models.PositiveSmallIntegerField()

    class Meta:
        ordering = ['-id']
