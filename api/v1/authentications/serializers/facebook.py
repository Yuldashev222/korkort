import requests
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from api.v1.accounts.serializers import ProfileMinSerializer


class FacebookSignInSerializer(serializers.Serializer):
    access_token = serializers.CharField(write_only=True)
    token = serializers.CharField(read_only=True)
    user = ProfileMinSerializer(read_only=True)

    def validate(self, attrs):
        fields = 'email,first_name,last_name'
        access_token = attrs['access_token']
        url = f'https://graph.facebook.com/v17.0/me?fields={fields}&access_token={access_token}'
        facebook_response = requests.get(url)

        if facebook_response.status_code != 200:
            raise ValidationError({'access_token': 'Invalid'})

        facebook_data = facebook_response.json()
        # user, created = CustomUser.objects.get_or_create(username=facebook_id)
        # if created:
        #     # user.first_name = id_info['given_name']
        #     # user.last_name = id_info['family_name']
        #     user.auth_provider = 'facebook'
        #     user.is_verified = True
        #     user.set_password(None)
        #
        # elif not user.is_active:
        #     raise AuthenticationFailed('User inactive')
        #
        # elif not user.is_verified:
        #     user.is_verified = True
        #
        # user.save()
        # CustomToken.objects.filter(user=user).delete()
        # token = CustomToken.objects.create(user=user)
        # attrs['token'] = token.key
        # attrs['user'] = user
        return attrs
