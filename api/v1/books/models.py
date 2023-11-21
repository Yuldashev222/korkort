from django.db import models
from ckeditor.fields import RichTextField
from django.core.validators import MinValueValidator, FileExtensionValidator


class Book(models.Model):
    ordering_number = models.PositiveSmallIntegerField(validators=[MinValueValidator(1)])
    language = models.ForeignKey('languages.Language', on_delete=models.PROTECT)
    title = models.CharField(max_length=300)

    class Meta:
        unique_together = ['ordering_number', 'language']
        verbose_name_plural = 'Books'

    def __str__(self):
        return self.title


class BookChapter(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    ordering_number = models.PositiveSmallIntegerField(validators=[MinValueValidator(1)])
    is_open = models.BooleanField(default=False)
    title = models.CharField(max_length=300)
    audio = models.FileField(upload_to='books/chapters/audios/', blank=True, null=True,
                             validators=[FileExtensionValidator(allowed_extensions=['mp3'])])
    content = RichTextField()

    class Meta:
        ordering = ['ordering_number']
        unique_together = ['book', 'ordering_number']
        verbose_name_plural = 'Chapters'

    def __str__(self):
        return f'{self.book} Chapter No {self.ordering_number}'


class BookChapterStudent(models.Model):
    chapter = models.ForeignKey(BookChapter, on_delete=models.CASCADE)
    student = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE)
    is_completed = models.BooleanField(default=False)

