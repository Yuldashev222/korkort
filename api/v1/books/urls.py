from django.urls import path

from .views import BookListAPIView, BookChapterDetailAPIView, BookChapterStudentAPIView

urlpatterns = [
    path('', BookListAPIView.as_view(), name='book-list'),
    path('chapters/<int:pk>/', BookChapterDetailAPIView.as_view(), name='book-chapter-detail'),
    path('chapters/completed/', BookChapterStudentAPIView.as_view(), name='student-chapter-completed')
]
