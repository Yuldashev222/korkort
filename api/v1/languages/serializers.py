from rest_framework import serializers
from api.v1.languages.models import Language


class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language
        fields = ['pk', 'name']
