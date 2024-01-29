from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated

from api.v1.accounts.permissions import IsStudent
from api.v1.reports.models import Report
from api.v1.reports.serializers import ReportSerializer


class ReportAPIView(CreateAPIView):
    permission_classes = (IsAuthenticated, IsStudent)
    queryset = Report.objects.all()
    serializer_class = ReportSerializer
