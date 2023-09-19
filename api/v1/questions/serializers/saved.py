from rest_framework import serializers


class StudentSavedQuestionSerializer(serializers.Serializer):
    pk = serializers.IntegerField()
