from django.urls import path

from .views import SavedQuestionStudentAPIVIew, SavedQuestionStudentDestroyAPIVIew

urlpatterns = [
    path('saved/', SavedQuestionStudentAPIVIew.as_view()),
    path('saved/delete/', SavedQuestionStudentDestroyAPIVIew.as_view()),
]
