from django.urls import path

from api.v1.lessons.views import LessonAPIView, LessonStudentStatisticsByDayAPIView
from api.v1.questions.views import LessonAnswerAPIView

urlpatterns = [
    path('', LessonAPIView.as_view({'get': 'list'})),
    path('<int:pk>/', LessonAPIView.as_view({'get': 'retrieve'})),
    path('statistics/', LessonStudentStatisticsByDayAPIView.as_view({'get': 'list'})),
    path('questions/answers/', LessonAnswerAPIView.as_view())
]
