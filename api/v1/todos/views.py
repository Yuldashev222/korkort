from django.core.cache import cache
from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.response import Response
from django.utils.translation import get_language
from rest_framework.permissions import IsAuthenticated

from api.v1.todos.models import Todo, TodoDetail, TodoStudent
from api.v1.general.utils import bubble_search
from api.v1.todos.serializers import TodoListSerializer, TodoStudentSerializer
from api.v1.general.paginations import CustomPageNumberPagination
from api.v1.accounts.permissions import IsStudent


class TodoListAPIView(ListAPIView):
    permission_classes = (IsAuthenticated, IsStudent)
    pagination_class = CustomPageNumberPagination
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
            for i in page_cache['results']:
                obj = bubble_search(i['pk'], 'todo_id', sort_list)
                i['is_completed'] = obj and obj['is_completed']
            return Response(page_cache)

        queryset = self.filter_queryset(self.get_queryset())
        page_q = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page_q, many=True)
        data = self.get_paginated_response(serializer.data)
        cache.set(page, data.data)
        return data


class TodoStudentAPIView(CreateAPIView):
    serializer_class = TodoStudentSerializer
