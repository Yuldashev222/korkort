from django.urls import path

from .views import ExamAnswerAPIView

urlpatterns = [
    path('answers/', ExamAnswerAPIView.as_view()),
]
