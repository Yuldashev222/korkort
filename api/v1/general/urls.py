from django.urls import path

from api.v1.general.views import GeneralPoliceAPIView, GeneralPrivacyAPIView

urlpatterns = [
    path('police/', GeneralPoliceAPIView.as_view()),
    path('privacy/', GeneralPrivacyAPIView.as_view()),
]
