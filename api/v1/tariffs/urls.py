from django.urls import path

from .views import TariffAPIView

urlpatterns = [
    path('', TariffAPIView.as_view({'get': 'list'}), name='tariff-list'),
    path('<int:pk>/', TariffAPIView.as_view({'get': 'retrieve'}), name='tariff-detail')
]
