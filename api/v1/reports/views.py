from rest_framework.generics import CreateAPIView

from api.v1.reports.models import Report
from api.v1.reports.serializers import ReportSerializer


class ReportAPIView(CreateAPIView):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer
