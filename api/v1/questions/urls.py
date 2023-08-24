from django.urls import path

from .views import SavedQuestionStudentAPIVIew, SavedQuestionStudentDestroyAPIVIew

urlpatterns = [
    path('saved/', SavedQuestionStudentAPIVIew.as_view()),
    path('saved/<int:pk>/', SavedQuestionStudentDestroyAPIVIew.as_view()),
]
