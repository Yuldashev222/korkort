from django.urls import path

from .views import ProfileAPIView


urlpatterns = [
    path('profile/', ProfileAPIView.as_view())
]
