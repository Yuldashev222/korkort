# from django.db import models
#
#
# class Book(models.Model):
#     language = models.ForeignKey('languages.Language', on_delete=models.PROTECT)
#     title = models.CharField(max_length=300)
#
#     class Meta:
#
#
#
# class BookChapter(models.Model):
#     book = models.ForeignKey(Book, on_delete=models.CASCADE)
#     title = models.CharField(max_length=300)
