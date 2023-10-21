from django.urls import path
from api.v1.swish.views import SwishCardAPIView, MinBonusMoneyAPIView

urlpatterns = [
    path('minimum-bonus-money/', MinBonusMoneyAPIView.as_view()),
    path('', SwishCardAPIView.as_view()),
]
