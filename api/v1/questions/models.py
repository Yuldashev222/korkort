from django.db import models
from ckeditor.fields import RichTextField
from django.core.cache import cache
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, FileExtensionValidator

from api.v1.general.services import normalize_text
from api.v1.questions.services import get_last_frame_number_and_duration


class Category(models.Model):
    ordering_number = models.PositiveSmallIntegerField(primary_key=True, unique=True, validators=[MinValueValidator(1)])
    image = models.ImageField(upload_to='categories/images/', max_length=300)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return f'Category No {self.ordering_number}'


class CategoryDetail(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    language = models.ForeignKey('languages.Language', on_delete=models.PROTECT)
    name = models.CharField(max_length=300)

    class Meta:
        unique_together = ['category', 'language']

    def __str__(self):
        return f'{self.language_id} Category No {self.category_id}'


class Question(models.Model):
    DIFFICULTY_LEVEL = [[1, 'easy'], [2, 'normal'], [3, 'hard']]

    lesson = models.ForeignKey('lessons.Lesson', on_delete=models.SET_NULL, blank=True, null=True)  # last
    ordering_number = models.PositiveSmallIntegerField(validators=[MinValueValidator(1)], default=100000)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    difficulty_level = models.PositiveSmallIntegerField(choices=DIFFICULTY_LEVEL, default=DIFFICULTY_LEVEL[0][0])

    image = models.ImageField(upload_to='questions/images/', blank=True, null=True, max_length=300)
    gif = models.FileField(upload_to='questions/gifs/', blank=True, null=True, max_length=300,
                           validators=[FileExtensionValidator(allowed_extensions=['gif'])])
    gif_last_frame_number = models.PositiveSmallIntegerField(default=0)
    gif_duration = models.FloatField(default=0)

    def clean(self):
        if self.gif and self.image:
            raise ValidationError('choice gif or image')

    def __str__(self):
        if self.lesson:
            return f'Question No {self.ordering_number}'
        return f'Question No {self.pk}'

    class Meta:
        unique_together = ['lesson', 'ordering_number']  # last
        verbose_name_plural = '  Questions'

    def save(self, *args, **kwargs):
        if self.gif:
            self.gif_last_frame_number, self.gif_duration = get_last_frame_number_and_duration(self.gif.path)
        else:
            self.gif_last_frame_number, self.gif_duration = (0, 0)

        super().save(*args, **kwargs)

    @classmethod
    def is_correct_question_id(cls, question_id, question_ids=None):
        if question_ids is None:
            question_ids = cls.get_question_ids()
            len_question_ids = cls.get_all_questions_count()
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
    def get_question_ids(cls):  # last
        question_ids = cache.get('question_ids')
        if question_ids is None:
            cls.set_redis()
            question_ids = cache.get('question_ids')
        return question_ids

    @classmethod
    def get_all_questions_count(cls):
        all_questions_count = cache.get('all_questions_count')
        if all_questions_count is None:
            cls.set_redis()
            all_questions_count = cache.get('all_questions_count')
        return all_questions_count

    @classmethod
    def set_redis(cls):
        question_ids = list(Question.objects.order_by('pk').values_list('pk', flat=True))
        cache.set('all_questions_count', len(question_ids))
        cache.set('question_ids', question_ids)


class QuestionDetail(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    language = models.ForeignKey('languages.Language', on_delete=models.PROTECT)
    text = RichTextField(verbose_name='question text', max_length=300)

    correct_variant = models.CharField(max_length=300)
    variant2 = models.CharField(max_length=300)
    variant3 = models.CharField(max_length=300, blank=True)
    variant4 = models.CharField(max_length=300, blank=True)

    answer = RichTextField(max_length=500)

    def __str__(self):
        return f'{self.language_id} {self.question}'

    class Meta:
        unique_together = ['question', 'language']
        verbose_name = 'Question Detail'
        verbose_name_plural = ' Question Details'

    def save(self, *args, **kwargs):
        self.text, self.answer = normalize_text(self.text, self.answer)
        super().save(*args, **kwargs)


class StudentWrongAnswer(models.Model):
    student = models.ForeignKey('accounts.CustomUser', on_delete=models.SET_NULL, null=True)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)

    class Meta:
        unique_together = ['student', 'question']
        verbose_name = 'Wrong Answer'
        verbose_name_plural = 'Wrong Answers'


class StudentCorrectAnswer(models.Model):
    student = models.ForeignKey('accounts.CustomUser', on_delete=models.SET_NULL, null=True)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Correct Answer'
        verbose_name_plural = 'Correct Answers'


class StudentSavedQuestion(models.Model):
    student = models.ForeignKey('accounts.CustomUser', on_delete=models.SET_NULL, null=True)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['question', 'student']
