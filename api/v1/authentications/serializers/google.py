from django.conf import settings
from django.utils.translation import gettext_lazy as _

from google.oauth2 import id_token
from google.auth.transport import requests as google_requests

from rest_framework import serializers
from rest_framework.exceptions import ValidationError, AuthenticationFailed

from api.v1.accounts.models import CustomUser
from api.v1.accounts.serializers import ProfileSerializer
from api.v1.authentications.models import CustomToken


class GoogleSignInSerializer(serializers.Serializer):
    id_token = serializers.CharField(write_only=True)
    token = serializers.CharField(max_length=40, read_only=True, default='')
    user = ProfileSerializer(read_only=True)

    def validate(self, attrs):
        token = attrs.get('id_token')
        try:
            id_info = id_token.verify_oauth2_token(token, google_requests.Request())
            if id_info['aud'] not in settings.SOCIAL_SIGN_IN_IDS:
                raise ValidationError({'msg': 'Invalid client ID.'})
        except Exception as e:
            raise ValidationError({'msg': str(e)})

        user, created = CustomUser.objects.get_or_create(email=id_info['email'])
        if created:
            user.first_name = id_info['given_name']
            user.last_name = id_info['family_name']
            user.auth_provider = 'google'
            user.is_verified = True
            user.set_password(None)

        elif not user.is_active:
            raise AuthenticationFailed(_('User inactive'))

        elif not user.is_verified:
            user.is_verified = True

        user.save()
        CustomToken.objects.filter(user=user).delete()
        token = CustomToken.objects.create(user=user)
        attrs['token'] = token.key
        attrs['user'] = user
        return attrs
