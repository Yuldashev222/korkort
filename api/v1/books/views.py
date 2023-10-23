from django.core.cache import cache
from rest_framework.generics import ListAPIView, RetrieveAPIView, get_object_or_404, CreateAPIView
from django.utils.translation import get_language
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api.v1.books.models import BookDetail, Book, BookChapterDetail, BookChapterStudent, BookChapter
from api.v1.books.serializers import BookListSerializer, BookDetailSerializer, BookChapterStudentSerializer

from api.v1.lessons.permissions import IsOpenOrPurchased
from api.v1.general.paginations import CustomPageNumberPagination
from api.v1.accounts.permissions import IsStudent


class BookPagination(CustomPageNumberPagination):
    page_size = 5


class BookListAPIView(ListAPIView):
    pagination_class = BookPagination
    permission_classes = (IsAuthenticated, IsStudent)  # last
    serializer_class = BookListSerializer
    queryset = Book.objects.filter(is_active=True).order_by('ordering_number')

    def get_serializer_context(self):
        language = get_language()
        ctx = super().get_serializer_context()
        ctx['book_title_list'] = BookDetail.objects.filter(language_id=language
                                                           ).values('book_id', 'title'
                                                                    ).order_by('book__ordering_number')

        ctx['chapters'] = BookChapterDetail.objects.filter(chapter__is_active=True, language_id=get_language()
                                                           ).values('title',
                                                                    'chapter_id',
                                                                    'chapter__is_open',
                                                                    'chapter__book_id',
                                                                    ).order_by('chapter__ordering_number')

        ctx['student_chapter_list'] = BookChapterStudent.objects.filter(student_id=self.request.user.id
                                                                        ).values('chapter_id', 'is_completed'
                                                                                 ).order_by('chapter__ordering_number')
        return ctx


class BookDetailAPIView(RetrieveAPIView):
    permission_classes = (IsAuthenticated, IsStudent, IsOpenOrPurchased)
    queryset = BookChapter.objects.filter(is_active=True)
    serializer_class = BookDetailSerializer

    def retrieve(self, request, *args, **kwargs):
        page = str(request.build_absolute_uri())
        page_cache = cache.get(page)
        if page_cache:
            try:
                chapter_student = BookChapterStudent.objects.get(chapter_id=self.kwargs[self.lookup_field],
                                                                 student_id=self.request.user.id)
                page_cache['is_completed'] = chapter_student.is_completed
            except BookChapterStudent.DoesNotExist:
                pass
            return Response(page_cache)

        instance = self.get_object()
        serializer = self.get_serializer(instance)
        cache.set(page, serializer.data)
        return Response(serializer.data)

    def get_object(self):
        chapter = super().get_object()
        obj = get_object_or_404(BookChapterDetail, chapter_id=chapter.id, language_id=get_language())
        try:
            chapter_student = BookChapterStudent.objects.get(chapter_id=chapter.id, student_id=self.request.user.id)
            obj.is_completed = chapter_student.is_completed
        except BookChapterStudent.DoesNotExist:
            obj.is_completed = False
        obj.is_open = chapter.is_open
        return obj


class BookChapterStudentAPIView(CreateAPIView):
    serializer_class = BookChapterStudentSerializer
