from django.urls import path

from api.v1.reports.views import ReportAPIView

urlpatterns = [
    path('', ReportAPIView.as_view()),
]
