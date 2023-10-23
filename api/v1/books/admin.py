from django.contrib import admin
from api.v1.books.models import Book, BookChapter, BookPart


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['ordering_number', 'language', 'title']
    list_display_links = ['ordering_number', 'language']
    list_filter = ['language', 'ordering_number']
    search_fields = ['title']


@admin.register(BookChapter)
class BookChapterAdmin(admin.ModelAdmin):
    list_display = ['ordering_number', 'book', 'is_open', 'title']
    list_display_links = ['ordering_number', 'book', 'title']
    list_filter = ['ordering_number', 'book', 'is_open']
    search_fields = ['title']


@admin.register(BookPart)
class BookPartAdmin(admin.ModelAdmin):
    list_display = ['book_chapter', 'ordering_number']
    list_display_links = list_display
    list_filter = ['book_chapter', 'ordering_number']
