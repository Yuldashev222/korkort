from django.urls import path

from .views import TariffAPIView

urlpatterns = [
    path('', TariffAPIView.as_view(), name='tariff-list'),
]
