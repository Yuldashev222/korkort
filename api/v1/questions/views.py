from django.conf import settings
from rest_framework.status import HTTP_201_CREATED, HTTP_413_REQUEST_ENTITY_TOO_LARGE
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from api.v1.questions.serializers import AnswerSerializer


class ExamAnswerAPIView(GenericAPIView):
    serializer_class = AnswerSerializer

    def post(self, request, *args, **kwargs):
        data = request.data
        try:
            if len(data.get('answers')) > settings.MAX_EXAM_QUESTION_ANSWERS:
                return Response(status=HTTP_413_REQUEST_ENTITY_TOO_LARGE)
        except TypeError:
            serializer = self.get_serializer(data=data)
            serializer.is_valid(raise_exception=True)
            data = serializer.save()
        return Response(data, status=HTTP_201_CREATED)
