from django.core.cache import cache
from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.response import Response
from django.utils.translation import get_language
from rest_framework.permissions import IsAuthenticated

from api.v1.general.utils import bubble_search
from api.v1.todos.models import Todo, TodoDetail, TodoStudent
from api.v1.todos.serializers import TodoListSerializer, TodoStudentSerializer
from api.v1.general.paginations import CustomPageNumberPagination
from api.v1.accounts.permissions import IsStudent


class TodoListAPIView(ListAPIView):
    permission_classes = (IsAuthenticated, IsStudent)
    pagination_class = CustomPageNumberPagination
    queryset = Todo.objects.order_by('ordering_number')
    serializer_class = TodoListSerializer

    def list(self, request, *args, **kwargs):
        page = str(request.build_absolute_uri())
        page_cache = cache.get(page)
        if page_cache:
            sort_list = TodoStudent.objects.filter(student_id=self.request.user.id
                                                   ).values('todo_id', 'is_completed').order_by('todo__ordering_number')
            for i in page_cache:
                obj = bubble_search(i['id'], 'todo_id', sort_list)
                if obj is not None:
                    i['is_completed'] = obj['is_completed']
                else:
                    i['is_completed'] = False
            return Response(page_cache)

        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        cache.set(page, serializer.data)
        return Response(serializer.data)

    def get_queryset(self):
        language = get_language()
        return TodoDetail.objects.filter(language_id=language).values('todo_id', 'title', 'text'
                                                                      ).order_by('todo__ordering_number')

    def get_serializer_context(self):
        ctx = super().get_serializer_context()
        ctx['student_todo_list'] = TodoStudent.objects.filter(student_id=self.request.user.id
                                                              ).values('todo_id', 'is_completed'
                                                                       ).order_by('todo__ordering_number')
        return ctx


class TodoStudentAPIView(CreateAPIView):
    serializer_class = TodoStudentSerializer
