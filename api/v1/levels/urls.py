from django.urls import path

from api.v1.levels.views import LevelAPIView

urlpatterns = [
    path('', LevelAPIView.as_view()),
]
