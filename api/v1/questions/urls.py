from django.urls import path

from .views import StudentSavedQuestionAPIView

urlpatterns = [
    path('saved/', StudentSavedQuestionAPIView.as_view()),
]
