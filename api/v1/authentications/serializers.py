import jwt
import string
import secrets
import requests
from django.conf import settings
from django.core.cache import cache
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth import authenticate
from django.utils.encoding import force_str
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.password_validation import validate_password

from google.oauth2 import id_token
from google.auth.transport import requests as google_requests

from rest_framework import serializers
from rest_framework.exceptions import ValidationError, AuthenticationFailed

from api.v1.accounts.models import CustomUser

from .models import CustomToken
from .tasks import send_confirm_link_email, send_password_reset_email
from ..accounts.serializers import ProfileSerializer


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'password']
        extra_kwargs = {
            'first_name': {'min_length': 3},
            'last_name': {'min_length': 3},
            'password': {'write_only': True, 'style': {'input_type': 'password'}}
        }

    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        token = default_token_generator.make_token(user)
        user.save()

        current_site = get_current_site(self.context['request'])
        send_confirm_link_email.delay(str(user), user.id, token, current_site.domain, user.email)
        return user


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
            raise AuthenticationFailed({'msg': 'User has not confirmed email address.'})

        if not user.is_active:
            raise AuthenticationFailed({'msg': 'User inactive or deleted.'})

        CustomToken.objects.filter(user=user).delete()
        token = CustomToken.objects.create(user=user)
        attrs['user'] = user
        attrs['token'] = token.key
        return attrs


class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        try:
            self.user = CustomUser.objects.get(email=value)
        except CustomUser.DoesNotExist:
            raise ValidationError('User does not exist')
        return value

    def save(self):
        token = default_token_generator.make_token(self.user)
        current_site = get_current_site(self.context['request'])
        send_password_reset_email.delay(user_id=self.user.id, token=token, domain=current_site.domain,
                                        email_address=self.user.email, link_type=self.validated_data.get('link_type'))


class PasswordResetCodeSerializer(PasswordResetSerializer):
    def save(self):
        code = ''.join(secrets.choice(string.digits) for _ in range(6))
        cache.set(f'{self.user.email}_reset_password', code, 60 * 60 * 10)
        current_site = get_current_site(self.context['request'])
        send_password_reset_email.delay(user_id=self.user.id, code=code, domain=current_site.domain,
                                        email_address=self.user.email, link_type=self.validated_data.get('link_type'))


class PasswordResetConfirmSerializer(serializers.Serializer):
    uid = serializers.CharField(write_only=True)
    token = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True,
                                         style={'input_type': 'password'},
                                         trim_whitespace=False,
                                         validators=[validate_password], allow_null=True)

    def validate(self, attrs):
        uid = attrs.get('uid')
        token = attrs.get('token')
        new_password = attrs.get('new_password')

        try:
            uid = force_str(urlsafe_base64_decode(uid))
            self.user = CustomUser.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, AttributeError, CustomUser.DoesNotExist):
            raise ValidationError('Invalid password reset link')

        if not new_password:
            raise ValidationError({'new_password': 'This field is required.'})

        form = SetPasswordForm(user=self.user, data={'new_password1': new_password, 'new_password2': new_password})
        if not form.is_valid():
            raise ValidationError(form.errors)

        if not default_token_generator.check_token(self.user, token):
            raise ValidationError('Invalid password reset link')

        return attrs

    def save(self):
        self.user.set_password(self.validated_data['new_password'])
        self.user.save()


class CodePasswordResetConfirmSerializer(PasswordResetConfirmSerializer):
    uid = None
    token = None
    code = serializers.CharField(write_only=True)
    email = serializers.EmailField(write_only=True)

    def validate(self, attrs):
        code = attrs['code']
        new_password = attrs.get('new_password')
        email = attrs['email']

        if not new_password:
            raise ValidationError({'new_password': 'This field is required.'})

        try:
            self.user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            raise ValidationError({'email': 'not found'})

        if cache.get(f'{email}_reset_password') != code:
            raise ValidationError({'code': 'not valid or expired'})

        form = SetPasswordForm(user=self.user, data={'new_password1': new_password, 'new_password2': new_password})
        if not form.is_valid():
            raise ValidationError(form.errors)

        return attrs

    def save(self):
        self.user.set_password(self.validated_data['new_password'])
        self.user.save()
        cache.delete(f'{self.user.email}_reset_password')


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
            user.from_google_auth = True
            user.first_name = id_info['given_name']
            user.last_name = id_info['family_name']
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


class FacebookSignInSerializer(serializers.Serializer):
    access_token = serializers.CharField(write_only=True)
    token = serializers.CharField(max_length=40, read_only=True)

    def validate(self, attrs):
        access_token = attrs.get('access_token')
        query_params = {
            'input_token': access_token,
            'access_token': f'{settings.FACEBOOK_CLIENT_ID}|{settings.FACEBOOK_CLIENT_SECRET}',
        }
        response = requests.get(url='https://graph.facebook.com/debug_token', params=query_params)

        if response.status_code != 200:
            raise ValidationError({'msg': 'Invalid access token.'})
        try:
            data = response.json()
            if not data.get('data', {}).get('is_valid'):
                raise ValidationError({'msg': 'Invalid access token.'})

            # Access token is valid, perform further actions
            # user_id = data['data']['user_id']
            # print(data['data'], '--------')
            # You can create or authenticate the user here

            # user, created = CustomUser.objects.get_or_create(email=id_info['email'])
            #
            # if created:
            #     user.from_google_auth = True
            #     user.first_name = id_info['given_name']
            #     user.last_name = id_info['family_name']
            #     user.is_verified = True
            #     user.set_password(None)
            #     user.save()
            # elif not user.is_active:
            #     raise AuthenticationFailed(_('User inactive'))
            # elif not user.is_verified:
            #     user.is_verified = True
            #     user.save()
            #
            # CustomToken.objects.filter(user=user).delete()
            # token = CustomToken.objects.create(user=user)
            # attrs['token'] = token.key
        except Exception as e:
            attrs['token'] = str(e)
        return attrs


class AppleSignInSerializer(serializers.Serializer):
    id_token = serializers.CharField(write_only=True)
    token = serializers.CharField(max_length=40, read_only=True, default='')

    def validate(self, attrs):
        id_token = attrs.get('id_token')

        # Verify the received id_token using Apple's public key
        apple_public_key = self.get_apple_public_key()
        try:
            decoded_token = jwt.decode(
                id_token,
                apple_public_key,
                algorithms=['ES256'],
                audience=settings.APPLE_TEAM_ID,
                issuer='https://appleid.apple.com',
            )

            # Extract necessary user information from the decoded token
            user_id = decoded_token.get('sub')
            email = decoded_token.get('email')

        except jwt.exceptions.InvalidTokenError:
            raise ValidationError({'msg': 'Invalid token'})

        return attrs

    def get_apple_public_key(self):
        # Fetch Apple's public key for token verification
        response = requests.get('https://appleid.apple.com/auth/keys')
        jwks = response.json()
        # Extract the public key for the relevant algorithm
        apple_public_key = jwt.algorithms.RSAAlgorithm.from_jwk(jwks['keys'][0])
        return apple_public_key
