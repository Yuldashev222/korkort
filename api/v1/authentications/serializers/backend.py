from django.contrib.auth import authenticate
from django.core.cache import cache
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site

from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed, PermissionDenied, ValidationError
from rest_framework.generics import get_object_or_404

from api.v1.accounts.models import CustomUser
from api.v1.accounts.serializers import ProfileSerializer
from api.v1.authentications.tasks import send_confirm_link_email
from api.v1.authentications.models import CustomToken


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'password']
        extra_kwargs = {'first_name': {'min_length': 3},
                        'last_name': {'min_length': 3},
                        'password': {'write_only': True,
                                     'trim_whitespace': False,
                                     'style': {'input_type': 'password'}}}

    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        token = default_token_generator.make_token(user)
        current_site = get_current_site(self.context['request'])
        send_confirm_link_email.delay(str(user), user.id, token, current_site.domain, user.email)
        return user


class ResendEmailVerifyLinkSerializer(serializers.Serializer):
    email = serializers.EmailField(write_only=True)

    def validate(self, attrs):
        email = attrs['email']

        attempt = cache.get(f'{email}_resend_email_verify_link')
        if not attempt:
            cache.set(f'{email}_resend_email_verify_link', 1, 60 * 60 * 24)
        elif attempt >= 3:
            raise PermissionDenied()
        else:
            cache.incr(f'{email}_resend_email_verify_link')

        user = get_object_or_404(CustomUser, email=email, is_staff=False, is_verified=False)
        if not user.is_active:
            raise ValidationError({'active': 'this account is not active'})
        token = default_token_generator.make_token(user)
        current_site = get_current_site(self.context['request'])
        send_confirm_link_email.delay(str(user), user.id, token, current_site.domain, user.email)
        return attrs


class AuthTokenSerializer(serializers.Serializer):
    email = serializers.EmailField(write_only=True)
    password = serializers.CharField(write_only=True, style={'input_type': 'password'}, trim_whitespace=False)
    token = serializers.CharField(read_only=True)
    user = ProfileSerializer(read_only=True)

    def validate(self, attrs):
        email = attrs['email']
        password = attrs['password']

        user = authenticate(request=self.context['request'], email=email, password=password)

        if not user:
            raise AuthenticationFailed({'msg': _('Unable to log in with provided credentials.')})

        if not user.is_verified:
            raise PermissionDenied({'verified': 'User has not confirmed email address.'})

        if not user.is_active:
            raise PermissionDenied({'active': 'User inactive or deleted.'})

        CustomToken.objects.filter(user=user).delete()
        token = CustomToken.objects.create(user=user)
        attrs['user'] = user
        attrs['token'] = token.key
        return attrs
