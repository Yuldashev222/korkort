from django.urls import path
from api.v1.swish.views import SwishCardAPIView, CalledStudentAndSwishTransactionAPIView

urlpatterns = [
    path('', SwishCardAPIView.as_view()),
    path('histories/', CalledStudentAndSwishTransactionAPIView.as_view())
]
