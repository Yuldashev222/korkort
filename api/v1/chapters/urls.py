from django.urls import path

from .views import ChapterAPIView

urlpatterns = [
    path('', ChapterAPIView.as_view()),
]
