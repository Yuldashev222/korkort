import string
import secrets
from django.core.cache import cache
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.password_validation import validate_password

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from api.v1.accounts.models import CustomUser
from api.v1.authentications.tasks import send_password_reset_email


class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        try:
            self.user = CustomUser.objects.get(email=value, is_verified=True, is_staff=False, is_active=True)
        except CustomUser.DoesNotExist as e:
            raise ValidationError(str(e))
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
                                         validators=[validate_password],
                                         allow_null=True)

    def validate(self, attrs):
        uid = attrs['uid']
        token = attrs['token']
        new_password = attrs['new_password']

        try:
            uid = force_str(urlsafe_base64_decode(uid))
            user = CustomUser.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, AttributeError, CustomUser.DoesNotExist):
            raise ValidationError('Invalid password reset link')

        form = SetPasswordForm(user=user, data={'new_password1': new_password, 'new_password2': new_password})
        if not form.is_valid():
            raise ValidationError(form.errors)

        if not default_token_generator.check_token(user, token):  # last time 10 minute
            raise ValidationError('Invalid password reset link')

        user.set_password(new_password)
        user.save()
        return attrs


class CodePasswordResetConfirmSerializer(PasswordResetConfirmSerializer):
    uid = None
    token = None
    code = serializers.CharField(write_only=True)
    email = serializers.EmailField(write_only=True)

    def validate(self, attrs):
        code = attrs['code']
        new_password = attrs.get('new_password')
        email = attrs['email']

        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            raise ValidationError({'email': 'not found'})

        if cache.get(f'{email}_reset_password') != code:
            raise ValidationError({'code': 'not valid or expired'})

        if new_password:
            form = SetPasswordForm(user=user, data={'new_password1': new_password, 'new_password2': new_password})
            if not form.is_valid():
                raise ValidationError(form.errors)

            user.set_password(new_password)
            user.save()
            if cache.get(f'{user.email}_reset_password'):
                cache.delete(f'{user.email}_reset_password')
        return attrs
