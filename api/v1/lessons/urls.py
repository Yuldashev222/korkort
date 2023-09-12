from django.urls import path

from api.v1.lessons.views import LessonAnswerAPIView, LessonAPIView, StudentLessonViewStatisticsAPIView

urlpatterns = [
    path('<int:pk>/', LessonAPIView.as_view({'get': 'retrieve'})),
    path('statistics/', StudentLessonViewStatisticsAPIView.as_view()),
    path('questions/answers/', LessonAnswerAPIView.as_view())
]
