from django.urls import path

from .views import CategoryExamAPIView, ExamStudentResult, CategoryExamAnswerAPIView, WrongQuestionsExamAPIView

urlpatterns = [
    path('', ExamStudentResult.as_view()),
    path('categories/answers/', CategoryExamAnswerAPIView.as_view()),
    path('categories/', CategoryExamAPIView.as_view()),
    path('wrongs/', WrongQuestionsExamAPIView.as_view()),
]
