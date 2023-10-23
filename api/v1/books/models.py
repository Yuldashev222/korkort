from django.db import models
from ckeditor.fields import RichTextField
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, FileExtensionValidator

from api.v1.general.services import normalize_text


class Book(models.Model):
    ordering_number = models.PositiveSmallIntegerField(validators=[MinValueValidator(1)])
    language = models.ForeignKey('languages.Language', on_delete=models.PROTECT)
    title = models.CharField(max_length=300)

    class Meta:
        unique_together = ['ordering_number', 'language']

    def __str__(self):
        return f'{self.language}: Book No {self.ordering_number}'


class BookChapter(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    ordering_number = models.PositiveSmallIntegerField(validators=[MinValueValidator(1)])
    is_open = models.BooleanField(default=False)
    title = models.CharField(max_length=300)
    audio = models.FileField(upload_to='books/chapters/audios/', blank=True, null=True,
                             validators=[FileExtensionValidator(allowed_extensions=['mp3'])])

    class Meta:
        ordering = ['ordering_number']
        unique_together = ['book', 'ordering_number']

    def __str__(self):
        return f'{self.book} Chapter No {self.ordering_number}'


class BookPart(models.Model):
    book_chapter = models.ForeignKey(BookChapter, on_delete=models.CASCADE)
    ordering_number = models.PositiveSmallIntegerField(validators=[MinValueValidator(1)])

    title = models.CharField(max_length=300, blank=True)
    image = models.ImageField(upload_to='books/images/', blank=True, null=True)
    text = RichTextField(max_length=1000, blank=True)
    green_text = RichTextField(max_length=1000, blank=True)
    yellow_text = RichTextField(max_length=1000, blank=True)
    red_text = RichTextField(max_length=1000, blank=True)

    def __str__(self):
        return f'{self.book_chapter} Part No {self.ordering_number}'

    class Meta:
        ordering = ['ordering_number']
        unique_together = ['book_chapter', 'ordering_number']

    def clean(self):
        if not (self.title or self.image or self.text or self.green_text or self.yellow_text or self.red_text):
            raise ValidationError('choice')

    def save(self, *args, **kwargs):
        self.title = normalize_text(self.title)[0]
        super().save(*args, **kwargs)


class BookChapterStudent(models.Model):
    chapter = models.ForeignKey(BookChapter, on_delete=models.CASCADE)
    student = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE)
    is_completed = models.BooleanField(default=False)

