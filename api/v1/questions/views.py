from django.conf import settings
from rest_framework.status import HTTP_201_CREATED, HTTP_413_REQUEST_ENTITY_TOO_LARGE, HTTP_400_BAD_REQUEST
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from api.v1.accounts.permissions import IsStudent
from api.v1.questions.serializers import ExamAnswerSerializer, LessonQuestionAnswerSerializer


class ExamAnswerAPIView(GenericAPIView):
    serializer_class = ExamAnswerSerializer
    permission_classes = (IsAuthenticated, IsStudent)

    def post(self, request, *args, **kwargs):
        data = request.data.copy()
        try:
            if len(data['answers']) > settings.MAX_EXAM_QUESTION_ANSWERS:
                return Response(status=HTTP_413_REQUEST_ENTITY_TOO_LARGE)
        except Exception as e:
            print(e)
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        data = serializer.save()
        return Response(data, status=HTTP_201_CREATED)


class LessonAnswerAPIView(ExamAnswerAPIView):
    serializer_class = LessonQuestionAnswerSerializer
