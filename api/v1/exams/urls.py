from django.urls import path

from .views import CategoryExamAPIView, ExamStudentResult, CategoryExamAnswerAPIView

urlpatterns = [
    path('', ExamStudentResult.as_view()),
    path('categories/answers/', CategoryExamAnswerAPIView.as_view()),
    path('categories/', CategoryExamAPIView.as_view())
]
