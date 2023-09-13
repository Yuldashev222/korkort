from django.urls import path

from .views import CategoryExamAPIView, ExamStudentResult, CategoryExamAnswerAPIView, WrongQuestionsExamAPIView, \
    WrongQuestionsExamAnswerAPIView

urlpatterns = [
    path('', ExamStudentResult.as_view()),
    path('categories/answers/', CategoryExamAnswerAPIView.as_view()),
    path('categories/', CategoryExamAPIView.as_view()),
    path('wrongs/', WrongQuestionsExamAPIView.as_view()),
    path('wrongs/answers/', WrongQuestionsExamAnswerAPIView.as_view()),
]
