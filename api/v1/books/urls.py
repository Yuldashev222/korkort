from django.urls import path

from .views import BookListAPIView, BookDetailAPIView, BookChapterStudentAPIView

urlpatterns = [
    path('', BookListAPIView.as_view(), name='book-list'),
    path('<int:pk>/', BookDetailAPIView.as_view(), name='book-detail'),
    path('chapters/completed/', BookChapterStudentAPIView.as_view(), name='student-chapter-completed')
]
