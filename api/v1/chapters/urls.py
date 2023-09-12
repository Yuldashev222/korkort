from django.urls import path

from .views import ChapterStudentAPIView

urlpatterns = [
    path('', ChapterStudentAPIView.as_view({'get': 'list'})),
    path('<int:pk>/', ChapterStudentAPIView.as_view({'get': 'retrieve'})),
]
