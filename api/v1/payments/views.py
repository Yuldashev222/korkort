from rest_framework.status import HTTP_200_OK
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated

from api.v1.payments.models import Order
from api.v1.accounts.permissions import IsStudent
from api.v1.payments.serializers import OrderSerializer, CheckCouponSerializer


class OrderAPIView(ReadOnlyModelViewSet):
    pagination_class = LimitOffsetPagination
    serializer_class = OrderSerializer
    permission_classes = (IsAuthenticated, IsStudent)

    def get_queryset(self):
        student = self.request.user
        if student.is_authenticated:
            return Order.objects.filter(student=self.request.user).order_by('-id')
        return Order.objects.none()


class CheckCouponAPIView(CreateAPIView):
    serializer_class = CheckCouponSerializer
    permission_classes = [IsAuthenticated, IsStudent]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=HTTP_200_OK)
