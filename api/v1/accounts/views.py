from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api.v1.accounts.permissions import IsStudent
from api.v1.accounts.serializers import ProfileSerializer


class ProfileAPIView(ListAPIView):
    permission_classes = [IsAuthenticated, IsStudent]
    serializer_class = ProfileSerializer

    def list(self, request, *args, **kwargs):
        student = self.request.user

        serializer = self.get_serializer(student)
        return Response(serializer.data)
