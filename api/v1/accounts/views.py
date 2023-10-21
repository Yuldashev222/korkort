from rest_framework import mixins
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated

from api.v1.accounts.permissions import IsStudent
from api.v1.accounts.serializers import ProfileSerializer, ProfileUpdateSerializer


class ProfileAPIView(mixins.ListModelMixin, mixins.UpdateModelMixin, GenericAPIView):
    permission_classes = (IsAuthenticated, IsStudent)
    serializer_class = ProfileUpdateSerializer

    def get_object(self):
        return self.request.user

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        student = self.get_object()
        serializer = ProfileSerializer(student, context={'request': request})
        return Response(serializer.data)
