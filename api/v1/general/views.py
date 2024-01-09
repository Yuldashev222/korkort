from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated

from api.v1.general.models import General


class GeneralPoliceAPIView(GenericAPIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        obj = General.objects.first()
        if obj:
            return Response({'police': obj.police})
        return Response({'police': ''})


class GeneralPrivacyAPIView(GenericAPIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        obj = General.objects.first()
        if obj:
            return Response({'privacy': obj.privacy})
        return Response({'privacy': ''})
