from django.urls import path

from api.v1.exams.views.saved import SavedQuestionsExamAPIView, SavedQuestionsExamAnswerAPIView
from api.v1.exams.views.wrongs import WrongQuestionsExamAPIView, WrongQuestionsExamAnswerAPIView
from api.v1.exams.views.general import ExamStudentResult
from api.v1.exams.views.categories import CategoryExamAnswerAPIView, CategoryExamAPIView

urlpatterns = [
    path('', ExamStudentResult.as_view()),
    path('saved/', SavedQuestionsExamAPIView.as_view()),
    path('wrongs/', WrongQuestionsExamAPIView.as_view()),
    path('categories/', CategoryExamAPIView.as_view()),
    path('saved/answers/', SavedQuestionsExamAnswerAPIView.as_view()),
    path('wrongs/answers/', WrongQuestionsExamAnswerAPIView.as_view()),
    path('categories/answers/', CategoryExamAnswerAPIView.as_view()),

]

