from rest_framework import mixins
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated

from api.v1.questions.models import StudentSavedQuestion
from api.v1.accounts.permissions import IsStudent
from api.v1.questions.serializers.saved import SavedQuestionCreateSerializer, SavedQuestionRetrieveSerializer


class SavedQuestionStudentAPIVIew(mixins.CreateModelMixin,
                                  mixins.ListModelMixin,
                                  GenericAPIView):
    permission_classes = (IsAuthenticated, IsStudent)

    def perform_create(self, serializer):
        serializer.save(student=self.request.user)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        if not request.query_params.get('language'):
            return Response([])
        return self.list(request, *args, **kwargs)

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return SavedQuestionCreateSerializer
        return SavedQuestionRetrieveSerializer

    def get_queryset(self):
        student = self.request.user
        return StudentSavedQuestion.objects.filter(student=student).order_by('-created_at')


class SavedQuestionStudentDestroyAPIVIew(DestroyAPIView):
    permission_classes = (IsAuthenticated, IsStudent)
    serializer_class = SavedQuestionRetrieveSerializer

    def get_queryset(self):
        student = self.request.user
        return StudentSavedQuestion.objects.filter(student=student)
