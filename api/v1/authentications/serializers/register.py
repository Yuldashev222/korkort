from rest_framework import serializers
from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _
from rest_framework.exceptions import AuthenticationFailed, PermissionDenied

from api.v1.accounts.models import CustomUser
from api.v1.authentications.models import CustomToken


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['name', 'email', 'password']
        extra_kwargs = {
            'name': {
                'min_length': 3
            },
            'password': {
                'write_only': True,
                'trim_whitespace': False,
                'style': {'input_type': 'password'}
            }
        }

    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        # token = default_token_generator.make_token(user)
        # current_site = get_current_site(self.context['request'])
        # send_confirm_link_email.delay(str(user), user.pk, token, current_site.domain, user.email)
        return user


# class ResendEmailVerifyLinkSerializer(serializers.Serializer):
#     email = serializers.EmailField(write_only=True)
#
#     def validate(self, attrs):
#         email = attrs['email']
#
#         user = get_object_or_404(CustomUser, email=email, is_staff=False, is_verified=False)
#         if not user.is_active:
#             raise ValidationError({'active': 'this account is not active'})
#
#         attempt = cache.get(f'{email}_resend_email_verify_link')
#         if not attempt:
#             cache.set(f'{email}_resend_email_verify_link', 1, 60 * 60 * 24)
#         elif attempt >= 3:
#             raise PermissionDenied()
#         else:
#             cache.incr(f'{email}_resend_email_verify_link')
#
#         token = default_token_generator.make_token(user)
#         current_site = get_current_site(self.context['request'])
#         send_confirm_link_email.delay(str(user), user.pk, token, current_site.domain, user.email)
#         return attrs


class AuthTokenSerializer(serializers.Serializer):
    email = serializers.EmailField(write_only=True)
    password = serializers.CharField(write_only=True, style={'input_type': 'password'}, trim_whitespace=False)
    token = serializers.CharField(read_only=True)

    def validate(self, attrs):
        email = attrs['email']
        password = attrs['password']

        user = authenticate(request=self.context['request'], email=email, password=password)

        if not user:
            raise AuthenticationFailed({'msg': _('Unable to log in with provided credentials.')})

        if not user.is_active_user:
            raise PermissionDenied({'msg': 'User has not confirmed email address.'})

        CustomToken.objects.filter(user=user).delete()
        token = CustomToken.objects.create(user=user)
        attrs['token'] = token.key
        return attrs


class SocialAuthTokenSerializer(AuthTokenSerializer):
    password = None
    avatar_id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(write_only=True)

    def validate(self, attrs):
        email = attrs['email']
        name = attrs['name']
        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            user = CustomUser.objects.create_user(email=email, name=name, password=None)
        else:
            if not user.is_active_user:
                raise PermissionDenied({'msg': 'User has not confirmed email address.'})

            if not user.is_verified:
                user.is_verified = True
                user.save()

        CustomToken.objects.filter(user=user).delete()
        token = CustomToken.objects.create(user=user)
        attrs['token'] = token.key
        attrs['avatar_id'] = user.avatar_id
        return attrs
