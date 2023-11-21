from django.urls import path

from .views import ProfileUpdateAPIView

urlpatterns = [
    path('profile/update/', ProfileUpdateAPIView.as_view())
]
