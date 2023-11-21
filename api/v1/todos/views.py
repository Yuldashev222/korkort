from django.core.cache import cache
from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.response import Response
from django.utils.translation import get_language
from rest_framework.permissions import IsAuthenticated

from api.v1.todos.models import TodoDetail, TodoStudent
from api.v1.general.utils import bubble_search
from api.v1.todos.serializers import TodoListSerializer, TodoStudentSerializer
from api.v1.accounts.permissions import IsStudent


class TodoListAPIView(ListAPIView):
    permission_classes = (IsAuthenticated, IsStudent)
    serializer_class = TodoListSerializer

    def get_queryset(self):
        return TodoDetail.objects.filter(language_id=get_language()).values('todo_id', 'title', 'text'
                                                                            ).order_by('todo__ordering_number')

    def get_serializer_context(self):
        ctx = super().get_serializer_context()
        ctx['student_todo_list'] = TodoStudent.objects.filter(student_id=self.request.user.pk
                                                              ).values('todo_id', 'is_completed'
                                                                       ).order_by('todo__ordering_number')
        return ctx

    def list(self, request, *args, **kwargs):
        page = str(request.build_absolute_uri())
        page_cache = cache.get(page)
        if page_cache:
            sort_list = TodoStudent.objects.filter(student_id=self.request.user.pk
                                                   ).values('todo_id', 'is_completed').order_by('todo__ordering_number')
            for i in page_cache:
                obj = bubble_search(i['pk'], 'todo_id', sort_list)
                i['is_completed'] = bool(obj and obj['is_completed'])
            return Response(page_cache)

        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        cache.set(page, serializer.data)
        return Response(serializer.data)


class TodoStudentAPIView(CreateAPIView):
    serializer_class = TodoStudentSerializer
