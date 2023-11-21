from rest_framework.generics import UpdateAPIView
from rest_framework.permissions import IsAuthenticated

from api.v1.accounts.permissions import IsStudent
from api.v1.accounts.serializers import ProfileUpdateSerializer


class ProfileUpdateAPIView(UpdateAPIView):
    permission_classes = (IsAuthenticated, IsStudent)
    serializer_class = ProfileUpdateSerializer

    def get_object(self):
        return self.request.user
