from django.conf import settings
from rest_framework import mixins
from rest_framework.status import HTTP_201_CREATED, HTTP_413_REQUEST_ENTITY_TOO_LARGE
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated

from api.v1.questions.models import SavedQuestionStudent
from api.v1.accounts.permissions import IsStudent
from api.v1.questions.serializers import (
    AnswerSerializer,
    StudentAnswerSerializer,
    SavedQuestionStudentCreateSerializer,
    SavedQuestionStudentRetrieveSerializer
)


class ExamAnswerAPIView(GenericAPIView):  # last
    serializer_class = AnswerSerializer
    permission_classes = (IsAuthenticated, IsStudent)

    def post(self, request, *args, **kwargs):
        data = request.data
        try:
            if len(data['answers']) > settings.MAX_QUESTION_ANSWERS:
                return Response(status=HTTP_413_REQUEST_ENTITY_TOO_LARGE)
        except Exception as e:
            print(e)
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        data = serializer.save()
        return Response(data, status=HTTP_201_CREATED)


class LessonAnswerAPIView(ExamAnswerAPIView):
    serializer_class = StudentAnswerSerializer


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
            return SavedQuestionStudentCreateSerializer
        return SavedQuestionStudentRetrieveSerializer

    def get_queryset(self):
        student = self.request.user
        return SavedQuestionStudent.objects.filter(student=student).order_by('-created_at')


class SavedQuestionStudentDestroyAPIVIew(DestroyAPIView):
    permission_classes = (IsAuthenticated, IsStudent)
    serializer_class = SavedQuestionStudentRetrieveSerializer

    def get_queryset(self):
        student = self.request.user
        return SavedQuestionStudent.objects.filter(student=student)
