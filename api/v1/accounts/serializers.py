from rest_framework import serializers

from api.v1.accounts.models import CustomUser


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'user_code', 'bonus_money']
