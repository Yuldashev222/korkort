from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.pagination import LimitOffsetPagination

from api.v1.payments.models import Order
from api.v1.payments.serializers import OrderSerializer


class OrderAPIView(ReadOnlyModelViewSet):
    pagination_class = LimitOffsetPagination
    serializer_class = OrderSerializer

    def get_queryset(self):
        return Order.objects.filter(student=self.request.user).order_by('-id')
