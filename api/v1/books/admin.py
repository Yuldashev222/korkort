from django.contrib import admin
from api.v1.books.models import Book, BookChapter


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['ordering_number', 'language', 'title']
    list_display_links = list_display
    list_filter = ['language']
    search_fields = ['title']
    ordering = ['ordering_number']


class BookFilter(admin.SimpleListFilter):
    title = 'Books'
    parameter_name = 'book'

    def lookups(self, request, model_admin):
        language_id = request.GET.get('book__language__id__exact')
        if language_id:
            books = Book.objects.filter(language_id=language_id).order_by('ordering_number')
            if books.exists():
                return ((book.pk, str(book)) for book in books)
        return ((None, None),)

    def queryset(self, request, queryset):
        book_id = self.value()
        language_id = request.GET.get('book__language__id__exact')
        if book_id and language_id:
            queryset = queryset.filter(book_id=book_id)
        return queryset


@admin.register(BookChapter)
class BookChapterAdmin(admin.ModelAdmin):
    list_display = ['ordering_number', 'book', 'is_open', 'title']
    list_display_links = ['ordering_number', 'book', 'title']
    list_filter = ('book__language', BookFilter, 'is_open')  # last
    search_fields = ['title', 'content']
