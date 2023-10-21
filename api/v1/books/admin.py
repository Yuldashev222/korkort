from django.contrib import admin
from api.v1.books.models import Book, BookDetail, BookChapter, BookChapterDetail, BookPart
from api.v1.general.admin import AbstractTabularInline, AbstractStackedInline


class BookDetailInline(AbstractTabularInline):
    model = BookDetail
    verbose_name = 'Title'
    verbose_name_plural = 'Titles'


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['ordering_number', 'is_active']
    inlines = (BookDetailInline,)


class BookChapterDetailInline(AbstractTabularInline):
    model = BookChapterDetail


@admin.register(BookChapter)
class BookChapterAdmin(admin.ModelAdmin):
    list_display = ['book', 'ordering_number', 'is_open', 'is_active']
    list_filter = list_display
    inlines = (BookChapterDetailInline,)


class BookPartInline(AbstractStackedInline):
    model = BookPart
    min_num = 1
    max_num = None
    extra = 3
    verbose_name = 'detail'
    verbose_name_plural = 'details'


@admin.register(BookChapterDetail)
class BookChapterDetailAdmin(admin.ModelAdmin):
    list_display = ['chapter', 'title', 'language', 'audio']
    list_display_links = ['chapter', 'title', 'language']
    list_filter = ['chapter', 'language']
    inlines = (BookPartInline,)
