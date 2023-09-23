from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated

from api.v1.swish.permissions import GtMinBonusMoney
from api.v1.swish.serializers import SwishCardSerializer
from api.v1.accounts.permissions import IsStudent


class SwishCardAPIView(CreateAPIView):
    permission_classes = (IsAuthenticated, IsStudent, GtMinBonusMoney)
    serializer_class = SwishCardSerializer
