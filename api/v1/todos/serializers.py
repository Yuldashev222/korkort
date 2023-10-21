from rest_framework import serializers

from api.v1.general.utils import bubble_search
from api.v1.todos.models import TodoStudent


class TodoListSerializer(serializers.Serializer):
    id = serializers.IntegerField(source='todo_id')
    title = serializers.CharField()
    text = serializers.CharField()
    is_completed = serializers.SerializerMethodField()

    def get_is_completed(self, instance):
        sort_list = self.context['student_todo_list']
        obj = bubble_search(instance['todo_id'], 'todo_id', sort_list)
        if obj is not None:
            return obj['is_completed']
        return False


class TodoStudentSerializer(serializers.ModelSerializer):
    student = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = TodoStudent
        fields = ['student', 'todo', 'is_completed']

    def create(self, validated_data):
        is_completed = validated_data.pop('is_completed')
        obj, _ = TodoStudent.objects.get_or_create(**validated_data)
        if obj.is_completed != is_completed:
            obj.is_completed = is_completed
            obj.save()
        return obj
