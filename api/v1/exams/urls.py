from django.urls import path

from api.v1.exams.views.final import FinalExamAPIView, FinalExamAnswerAPIView
from api.v1.exams.views.saved import SavedQuestionsExamAPIView, SavedQuestionsExamAnswerAPIView
from api.v1.exams.views.wrongs import WrongQuestionsExamAPIView, WrongQuestionsExamAnswerAPIView
from api.v1.exams.views.general import CategoryResultAPIView

from api.v1.exams.views.categories import (CategoryExamAnswerAPIView, CategoryExamAPIView, CategoryMixExamAPIView,
                                           CategoryMixExamAnswerAPIView)

urlpatterns = [
    path('', CategoryResultAPIView.as_view()),
    path('saved/', SavedQuestionsExamAPIView.as_view()),
    path('final/', FinalExamAPIView.as_view()),
    path('wrongs/', WrongQuestionsExamAPIView.as_view()),
    path('categories/', CategoryExamAPIView.as_view()),
    path('final/answers/', FinalExamAnswerAPIView.as_view()),
    path('saved/answers/', SavedQuestionsExamAnswerAPIView.as_view()),
    path('categories/mix/', CategoryMixExamAPIView.as_view()),
    path('wrongs/answers/', WrongQuestionsExamAnswerAPIView.as_view()),
    path('categories/answers/', CategoryExamAnswerAPIView.as_view()),
    path('categories/mix/answers/', CategoryMixExamAnswerAPIView.as_view())
]
