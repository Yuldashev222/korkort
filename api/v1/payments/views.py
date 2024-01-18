from rest_framework.status import HTTP_200_OK
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.permissions import IsAuthenticated

from api.v1.payments.models import Order
from api.v1.general.paginations import CustomPageNumberPagination
from api.v1.accounts.permissions import IsStudent
from api.v1.payments.serializers import OrderSerializer, CheckCouponSerializer


class OrderAPIView(ReadOnlyModelViewSet):
    pagination_class = CustomPageNumberPagination
    serializer_class = OrderSerializer
    permission_classes = (IsAuthenticated, IsStudent)

    def get_queryset(self):
        return Order.objects.filter(student_email=self.request.user.email).order_by('-created_at')  # last is_paid=True


class CheckCouponAPIView(CreateAPIView):
    serializer_class = CheckCouponSerializer
    permission_classes = (IsAuthenticated, IsStudent)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=HTTP_200_OK)
