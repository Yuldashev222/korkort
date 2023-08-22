from django.urls import path

from .views import LessonAPIView, LessonStudentStatisticsByDayAPIView

urlpatterns = [
    path('', LessonAPIView.as_view({'get': 'list'})),
    path('<int:pk>/', LessonAPIView.as_view({'get': 'retrieve'})),
    path('statistics/', LessonStudentStatisticsByDayAPIView.as_view({'get': 'list'}))
]
