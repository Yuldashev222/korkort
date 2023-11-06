from rest_framework.response import Response
from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import IsAuthenticated

from api.v1.swish.models import MinBonusMoney
from api.v1.swish.serializers import SwishCardSerializer
from api.v1.accounts.permissions import IsStudent


class SwishCardAPIView(ListCreateAPIView):
    permission_classes = (IsAuthenticated, IsStudent)
    serializer_class = SwishCardSerializer

    def get(self, request, *args, **kwargs):
        return Response({'min_bonus_money': MinBonusMoney.get_min_bonus_money()})
