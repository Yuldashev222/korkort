from random import randint

from django.db import models, OperationalError
from django.core.cache import cache
from django.core.validators import MinValueValidator, FileExtensionValidator

from api.v1.general.services import normalize_text
from api.v1.questions.services import (category_image_location, question_image_location, question_gif_location,
                                       get_last_frame_number_and_duration)


class Category(models.Model):
    name_swe = models.CharField(max_length=300)
    name_en = models.CharField(max_length=300, blank=True)
    name_e_swe = models.CharField(max_length=300, blank=True)
    image = models.ImageField(upload_to=category_image_location, max_length=300)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name_swe[:30]


class Question(models.Model):
    DIFFICULTY_LEVEL = [
        [1, 'easy'], [2, 'normal'], [3, 'hard']
    ]
    lesson = models.ForeignKey('lessons.Lesson', on_delete=models.SET_NULL, blank=True, null=True)
    ordering_number = models.PositiveSmallIntegerField(validators=[MinValueValidator(1)], blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    difficulty_level = models.PositiveSmallIntegerField(choices=DIFFICULTY_LEVEL, default=DIFFICULTY_LEVEL[0][0])

    answer = models.CharField(max_length=500, blank=True)

    text_en = models.CharField(max_length=300, verbose_name='English', blank=True)
    text_swe = models.CharField(max_length=300, verbose_name='Swedish')
    text_e_swe = models.CharField(max_length=300, verbose_name='Easy Swedish', blank=True)

    gif = models.FileField(upload_to=question_gif_location, blank=True, null=True, max_length=300,
                           validators=[FileExtensionValidator(allowed_extensions=['gif'])])
    gif_last_frame_number = models.PositiveSmallIntegerField(default=0)
    gif_duration = models.PositiveSmallIntegerField(default=0)
    image = models.ImageField(upload_to=question_image_location, blank=True, null=True, max_length=300)

    @classmethod
    def is_correct_question_id(cls, question_id, question_ids=None):
        if question_ids is None:
            question_ids = cls.get_question_ids()
            len_question_ids = cache.get('all_questions_count')
        else:
            len_question_ids = len(question_ids)

        left, right = 0, len_question_ids - 1

        while left <= right:
            mid = (left + right) // 2
            if question_ids[mid] == question_id:
                return True
            elif question_ids[mid] < question_id:
                left = mid + 1
            else:
                right = mid - 1

        return False

    @classmethod
    def get_question_ids(cls):
        question_ids = cache.get('question_ids')
        if not question_ids:
            cls.set_redis()
            question_ids = cache.get('question_ids')
        return question_ids

    @classmethod
    def get_all_questions_count(cls):
        all_questions_count = cache.get('all_questions_count')
        if not all_questions_count:
            try:
                cls.set_redis()
            except OperationalError:
                return 0
            all_questions_count = cache.get('all_questions_count')
        return all_questions_count

    def __str__(self):
        return f'{self.id}: {self.text_swe}'[:30]

    class Meta:
        ordering = ['ordering_number']
        unique_together = ['lesson', 'ordering_number']

    def save(self, *args, **kwargs):
        self.text_swe, self.text_en, self.text_e_swe, self.answer = normalize_text(self.text_swe, self.text_en,
                                                                                   self.text_e_swe, self.answer)

        if not self.lesson:
            self.ordering_number = 100000

        if self.gif:
            self.gif_last_frame_number, self.gif_duration = get_last_frame_number_and_duration(self.gif.path)
        else:
            self.gif_last_frame_number, self.gif_duration = (0, 0)

        super().save(*args, **kwargs)

    @classmethod
    def set_redis(cls):
        question_ids = list(Question.objects.order_by('id').values_list('id', flat=True))
        cache.set('all_questions_count', len(question_ids), 60 * 60 * 24 * 30)
        cache.set('question_ids', question_ids, 60 * 60 * 24 * 30)


class Variant(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)

    is_correct = models.BooleanField(default=False)

    text_swe = models.CharField(max_length=300, verbose_name='Swedish')
    text_en = models.CharField(max_length=300, verbose_name='English', blank=True)
    text_e_swe = models.CharField(max_length=300, verbose_name='Easy Swedish', blank=True)

    def save(self, *args, **kwargs):
        self.text_swe, self.text_en, self.text_e_swe = normalize_text(self.text_swe, self.text_en, self.text_e_swe)
        super().save(*args, **kwargs)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['question'], condition=models.Q(is_correct=True),
                                    name="Each question must have exactly one correct option.")
        ]


class StudentWrongAnswer(models.Model):
    student = models.ForeignKey('accounts.CustomUser', on_delete=models.SET_NULL, null=True)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)

    class Meta:
        unique_together = ['student', 'question']
        verbose_name = 'Wrong Answer'
        verbose_name_plural = 'Wrong Answers'

    def __str__(self):
        return str(self.question)


class StudentCorrectAnswer(models.Model):
    student = models.ForeignKey('accounts.CustomUser', on_delete=models.SET_NULL, null=True)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Correct Answer'
        verbose_name_plural = 'Correct Answers'

    def __str__(self):
        return str(self.question)


class StudentSavedQuestion(models.Model):
    student = models.ForeignKey('accounts.CustomUser', on_delete=models.SET_NULL, null=True)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.question)

    class Meta:
        ordering = ['-created_at']
        unique_together = ['question', 'student']
