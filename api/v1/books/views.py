from django.core.cache import cache
from rest_framework.response import Response
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView
from django.utils.translation import get_language
from rest_framework.permissions import IsAuthenticated

from api.v1.books.models import BookChapterStudent, BookChapter, Book
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

    def get_queryset(self):
        return Book.objects.filter(language=get_language()).prefetch_related('bookchapter_set'
                                                                             ).order_by('ordering_number')

    def get_serializer_context(self):
        ctx = super().get_serializer_context()
        ctx['student_chapter_list'] = BookChapterStudent.objects.filter(student_id=self.request.user.id
                                                                        ).values('chapter_id', 'is_completed'
                                                                                 ).order_by('chapter__ordering_number')
        return ctx


class BookDetailAPIView(RetrieveAPIView):
    permission_classes = (IsAuthenticated, IsStudent, IsOpenOrPurchased)
    queryset = BookChapter.objects.all()
    serializer_class = BookDetailSerializer

    def retrieve(self, request, *args, **kwargs):
        page = str(request.build_absolute_uri())
        page_cache = cache.get(page)
        if page_cache:
            try:
                chapter_student, _ = BookChapterStudent.objects.get_or_create(chapter_id=self.kwargs[self.lookup_field],
                                                                              student_id=self.request.user.id)
                page_cache['is_completed'] = chapter_student.is_completed
            except BookChapterStudent.DoesNotExist:
                pass
            return Response(page_cache)

        instance = self.get_object()
        serializer = self.get_serializer(instance)
        cache.set(page, serializer.data)
        return Response(serializer.data)


class BookChapterStudentAPIView(CreateAPIView):
    serializer_class = BookChapterStudentSerializer
