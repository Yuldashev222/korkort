from rest_framework.generics import ListAPIView, RetrieveAPIView, get_object_or_404, CreateAPIView
from django.utils.translation import get_language
from rest_framework.permissions import IsAuthenticated

from api.v1.books.models import BookDetail, Book, BookChapterDetail, BookChapterStudent, BookChapter
from api.v1.books.serializers import BookListSerializer, BookDetailSerializer, BookChapterStudentSerializer

from api.v1.accounts.permissions import IsStudent


class BookListAPIView(ListAPIView):
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
                                                           ).values('chapter_id', 'chapter__book_id', 'title'
                                                                    ).order_by('chapter__ordering_number')

        ctx['student_chapter_list'] = BookChapterStudent.objects.filter(student_id=self.request.user.id
                                                                        ).values('chapter_id', 'is_completed'
                                                                                 ).order_by('chapter__ordering_number')
        return ctx


class BookDetailAPIView(RetrieveAPIView):
    permission_classes = (IsAuthenticated, IsStudent)  # last
    queryset = BookChapter.objects.filter(is_active=True)
    serializer_class = BookDetailSerializer

    def get_object(self):
        chapter = super().get_object()
        obj = get_object_or_404(BookChapterDetail, chapter_id=chapter.id, language_id=get_language())
        try:
            chapter_student = BookChapterStudent.objects.get(chapter_id=chapter.id, student_id=self.request.user.id)
            obj.is_completed = chapter_student.is_completed
        except BookChapterStudent.DoesNotExist:
            obj.is_completed = False
        return obj


class BookChapterStudentAPIView(CreateAPIView):
    serializer_class = BookChapterStudentSerializer
