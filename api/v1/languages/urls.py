from django.urls import path

from api.v1.languages.views import LanguageAPIView

urlpatterns = [
    path('', LanguageAPIView.as_view()),
]
