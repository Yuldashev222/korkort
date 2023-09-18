from django.urls import path

from api.v1.swish.views import SwishCardAPIView

urlpatterns = [
    path('', SwishCardAPIView.as_view())
]
